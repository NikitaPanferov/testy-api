from sqlalchemy import ForeignKey, Integer, UniqueConstraint, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class Answer(Base):
    text: Mapped[str] = mapped_column(String(255))
    is_correct: Mapped[bool]
    number_in_question: Mapped[int]
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), nullable=False)
    is_users: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Отношение к вопросам
    question = relationship("Question", back_populates="answers")

    __table_args__ = (
        UniqueConstraint('question_id', 'number_in_question', name='_question_number_uc'),
    )