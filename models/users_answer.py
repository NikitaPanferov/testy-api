from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class UsersAnswer(Base):

    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), nullable=False)
    is_correct: Mapped[bool]

    # Отношение к вопросам
    question = relationship("Question", back_populates="users_answers")
