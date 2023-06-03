from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, MetaData, String, Text
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship, validates)
from sqlalchemy_fields.types import URLType
from typing_extensions import Annotated

posts_metadata = MetaData()
intpk = Annotated[int, mapped_column(primary_key=True)]


Base = declarative_base(metadata=posts_metadata)


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[intpk]
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_verified = mapped_column(Boolean, default=False, nullable=False)
    mediafiles = relationship('MediaFile',
                              back_populates='post')
    target_channel_id = mapped_column(Integer,
                                      ForeignKey('target.id'), nullable=False)
    target = relationship('Target', back_populates='posts')

    @validates('text')
    def validate_field1(self, key, value):
        if not value and not self.mediafiles:
            raise AssertionError('Хотя бы одно из полей должно быть заполнено')
        return value

    @validates('mediafiles')
    def validate_field2(self, key, value):
        if not self.text and not value:
            raise AssertionError('Хотя бы одно из полей должно быть заполнено')
        return value


class MediaFile(Base):
    __tablename__ = 'mediafile'

    id: Mapped[intpk]
    path = mapped_column(String)
    url = mapped_column(URLType)
    post_id = mapped_column(Integer, ForeignKey('post.id'))
    post = relationship(Post, back_populates='mediafiles')

    def __str__(self) -> str:
        return str(self.path.split('/')[-1])


class Target(Base):
    __tablename__ = 'target'

    id: Mapped[intpk]
    telegram_id = mapped_column(String)
    name = mapped_column(String)
    active = mapped_column(Boolean, default=False, nullable=False)
    forwarding = mapped_column(Boolean, default=False, nullable=False)
    channels = relationship('Channel', back_populates='target', lazy='select')
    posts = relationship(Post, back_populates='target')

    def __str__(self) -> str:
        return self.name if self.name else str(self.telegram_id)


class Channel(Base):
    __tablename__ = 'channel'

    id: Mapped[intpk]
    telegram_id = mapped_column(String)
    name = mapped_column(String)
    target_id = mapped_column(Integer, ForeignKey('target.id'))
    target = relationship(Target, back_populates='channels')

    def __str__(self):
        return self.name if self.name else str(self.telegram_id)
