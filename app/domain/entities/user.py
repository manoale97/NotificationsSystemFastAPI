from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    id: int | None
    name: str
    email: str
    is_active: bool = True
