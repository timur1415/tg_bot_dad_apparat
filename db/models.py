from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    machine_info: Mapped[str] = mapped_column(String, nullable=False)
    problem: Mapped[str] = mapped_column(String, nullable=False)
    table_error: Mapped[str | None] = mapped_column(String, nullable=True)
    amount: Mapped[str | None] = mapped_column(String, nullable=True)
    requisites: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
