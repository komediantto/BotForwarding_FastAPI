from sqlalchemy import Integer, MetaData, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

tgsession_metadata = MetaData()

Base = declarative_base(metadata=tgsession_metadata)


class TgSession(Base):
    __tablename__ = "tgsession"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)
    session_string: Mapped[str] = mapped_column(String, unique=True)
