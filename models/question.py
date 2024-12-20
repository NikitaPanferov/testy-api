from enum import Enum
from typing import Optional

from sqlalchemy import Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class QuestionTypeEnum(Enum):
    oneChoice = 'oneChoice'
    multiChoice = 'multiChoice'
    answer = 'answer'


question_type_enum = ENUM('oneChoice', 'multiChoice', 'answer', name='question_type')


class Question(Base):
    text: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[QuestionTypeEnum] = mapped_column(question_type_enum)
    number_in_test: Mapped[int]
    test_id: Mapped[int] = mapped_column(Integer, ForeignKey('forms.id'), nullable=False)

    # Отношения
    form = relationship("Form", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    users_answers = relationship("UsersAnswer", back_populates="question", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('test_id', 'number_in_test', name='_test_number_uc'),
    )