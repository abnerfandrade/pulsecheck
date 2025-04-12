from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from app.models.base import Base

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
    frequency: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"Service(" \
            f"id={self.id!r}," \
            f"name={self.name!r}," \
            f"url={self.url!r}," \
            f"frequency={self.frequency!r}," \
            f"created_at={self.created_at!r}" \
        ")"
