import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
