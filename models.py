from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class Recipes(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    count_watch: Mapped[int] = mapped_column(Integer, default=0)
    time_cooking: Mapped[int] = mapped_column(Integer)
    ingredient: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
