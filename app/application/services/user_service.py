from app.domain.entities.user import User
from app.domain.errors import EmailAlreadyExistsError, UserNotFoundError
from app.domain.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, name: str, email: str) -> User:
        if self.repository.get_by_email(email) is not None:
            raise EmailAlreadyExistsError(email)
        return self.repository.create(User(id=None, name=name, email=email))

    def list_users(self) -> list[User]:
        return self.repository.list()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def update_user(
        self, user_id: int, name: str, email: str, is_active: bool
    ) -> User:
        current_user = self.get_user(user_id)
        existing_email_user = self.repository.get_by_email(email)
        if existing_email_user is not None and existing_email_user.id != user_id:
            raise EmailAlreadyExistsError(email)

        updated_user = User(
            id=current_user.id,
            name=name,
            email=email,
            is_active=is_active,
        )
        return self.repository.update(updated_user)

    def delete_user(self, user_id: int) -> None:
        self.get_user(user_id)
        self.repository.delete(user_id)
