from datetime import date

from sqlalchemy import Integer, MetaData, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

users_metadata = MetaData()

Base = declarative_base(metadata=users_metadata)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    created: Mapped[date]
    is_active: Mapped[bool]
