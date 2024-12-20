from typing import Optional

from sqlalchemy import Column, String, LargeBinary, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text)

    forms = relationship("Form", back_populates="user")
