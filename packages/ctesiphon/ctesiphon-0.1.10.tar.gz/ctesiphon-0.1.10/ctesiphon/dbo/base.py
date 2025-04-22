from typing import TypeVar

from pydantic import BaseModel

from ..enums import CacheTypes


class BaseDBO(BaseModel):
    __cache_type__: CacheTypes = CacheTypes.NONE
    __cache_expiration__: int = 0

    @classmethod
    def get_fields(cls) -> list[str]:
        return [ field_name for field_name, _ in cls.model_fields.items() ]

    def __hash__(self) -> int:
        return hash(self.model_dump_json())


ModelDBOType = TypeVar('ModelDBOType', bound=BaseDBO)
