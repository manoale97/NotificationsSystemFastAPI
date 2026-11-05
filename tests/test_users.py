from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False
    )
    Base.metadata.create_all(bind=engine)

    def get_test_db() -> Iterator[Session]:
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_user_crud(client: TestClient) -> None:
    created = client.post(
        "/users",
        json={"name": "Ada Lovelace", "email": "ada@example.com"},
    )
    assert created.status_code == 201
    user = created.json()
    assert user == {
        "id": 1,
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "is_active": True,
    }

    assert client.get("/users").json() == [user]
    assert client.get("/users/1").json() == user

    updated = client.put(
        "/users/1",
        json={
            "name": "Ada",
            "email": "ada@example.com",
            "is_active": False,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Ada"
    assert updated.json()["is_active"] is False

    deleted = client.delete("/users/1")
    assert deleted.status_code == 204
    assert client.get("/users/1").status_code == 404


def test_user_validation_and_duplicate_email(client: TestClient) -> None:
    invalid_email = client.post(
        "/users",
        json={"name": "Ada", "email": "not-an-email"},
    )
    assert invalid_email.status_code == 422

    payload = {"name": "Ada", "email": "ada@example.com"}
    assert client.post("/users", json=payload).status_code == 201
    assert client.post("/users", json=payload).status_code == 409
