from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, String, Text, DateTime, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    posted: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    category: Mapped[PostCategory] = mapped_column(
        SAEnum(PostCategory, name="post_category"),
        default=PostCategory.NEWS,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(20),
        default="Anonymous",
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<Post id={self.id} "
            f"title={self.title!r} "
            f"category={self.category.value!r} "
            f"is_active={self.is_active} "
            f"author={self.author!r}>"
        )
