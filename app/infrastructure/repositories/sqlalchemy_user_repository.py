from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.infrastructure.models.user_model import UserModel


class SqlAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user: User) -> User:
        model = UserModel(name=user.name, email=user.email, is_active=user.is_active)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, user_id: int) -> User | None:
        model = self.session.get(UserModel, user_id)
        return self._to_entity(model) if model is not None else None

    def get_by_email(self, email: str) -> User | None:
        model = self.session.scalar(select(UserModel).where(UserModel.email == email))
        return self._to_entity(model) if model is not None else None

    def list(self) -> list[User]:
        models = self.session.scalars(select(UserModel).order_by(UserModel.id)).all()
        return [self._to_entity(model) for model in models]

    def update(self, user: User) -> User:
        model = self.session.get(UserModel, user.id)
        if model is None:
            raise RuntimeError("User disappeared while being updated")
        model.name = user.name
        model.email = user.email
        model.is_active = user.is_active
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, user_id: int) -> None:
        model = self.session.get(UserModel, user_id)
        if model is None:
            raise RuntimeError("User disappeared while being deleted")
        self.session.delete(model)
        self.session.commit()

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            is_active=model.is_active,
        )
