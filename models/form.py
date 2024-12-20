from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class Form(Base):
    title: Mapped[str] = mapped_column(String(255))
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Отношение к вопросам
    questions = relationship("Question", back_populates="form", cascade="all, delete-orphan")
    user = relationship("User", back_populates="forms")
