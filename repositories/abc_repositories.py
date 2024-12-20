from abc import ABC, abstractmethod
from typing import Optional, List

from models import User, Form, UsersAnswer
from schemas.form_schemas import QuestionSchema


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(
        self, email: str, name: str, hashed_password: bytes
    ) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def update_refresh_token(self, user_id: int, refresh_token: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        raise NotImplementedError()


class AbstractFormRepository(ABC):
    @abstractmethod
    async def get_tests_by_user_id(self, user_id: int) -> Optional[List[Form]]:
        raise NotImplementedError()

    @abstractmethod
    async def get_test_by_id(self, test_id: int) -> Optional[Form]:
        raise NotImplementedError()

    @abstractmethod
    async def create_test(self, title: str, user_id: int, questions: List[QuestionSchema], is_open: bool) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def get_right_answers(self, test_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def delete_form(self, test_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_test_id(self, test_id: int) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def update_test(self, test_id: int, test_title: str, questions: List[QuestionSchema]):
        raise NotImplementedError()

    @abstractmethod
    async def set_is_open(self, test_id: int, is_open: bool) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def create_users_answers(self, user_id, answers):
        raise NotImplementedError()
