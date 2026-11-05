from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.application.services.user_service import UserService
from app.infrastructure.database import get_db
from app.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(SqlAlchemyUserRepository(db))


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserServiceDependency) -> UserRead:
    return service.create_user(name=payload.name, email=str(payload.email))


@router.get("", response_model=list[UserRead])
def list_users(service: UserServiceDependency) -> list[UserRead]:
    return service.list_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserServiceDependency) -> UserRead:
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, payload: UserUpdate, service: UserServiceDependency
) -> UserRead:
    return service.update_user(
        user_id=user_id,
        name=payload.name,
        email=str(payload.email),
        is_active=payload.is_active,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserServiceDependency) -> Response:
    service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
