from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from jjnt_api.database import BaseModel


class Indicator(BaseModel):
    __tablename__ = "indicators"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    abbreviation: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    default_source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"))
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="indicators")


class Category(BaseModel):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    icon: Mapped[str] = mapped_column(nullable=False, unique=True)
    indicators: Mapped[list["Indicator"]] = relationship(back_populates="category", order_by=Indicator.id)
