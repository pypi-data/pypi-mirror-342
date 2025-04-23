from datetime import datetime
from typing import TypeVar

from pydantic import UUID4

from .base import BaseDBO


class RethinkDBBaseDBO(BaseDBO):
    __tablename__: str = "objects"
    __indexes__: list[str] = []

    id: UUID4 | None = None
    created_dt: datetime | None = None
    updated_dt: datetime | None = None

    @classmethod
    def get_fields(cls) -> list[str]:
        return [ field_name for field_name, _ in cls.model_fields.items() ]


ModelDBOType = TypeVar('ModelDBOType', bound=RethinkDBBaseDBO)
