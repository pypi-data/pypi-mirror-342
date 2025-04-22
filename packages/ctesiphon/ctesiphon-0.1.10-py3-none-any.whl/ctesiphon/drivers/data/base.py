from typing import Any, Type, Dict

from ...dbo.base import ModelDBOType


class BaseDBODriver:
    def __init__(self,
        dsn: str | None = None,
    ):
        self.dsn = dsn

    async def connect(self):
        raise NotImplementedError()
    
    async def disconnect(self):
        raise NotImplementedError()

    async def is_connected(self) -> bool:
        raise NotImplementedError()
    
    async def init_model(self, dbo_cls: ModelDBOType):
        raise NotImplementedError()
    
    async def create_model(self, dbo_cls: ModelDBOType):
        raise NotImplementedError()
    
    async def get_models_list(self) -> list[str]:
        raise NotImplementedError()
    
    async def rename_model(self, old_name: str, new_name: str):
        raise NotImplementedError()

    async def save(self, dbo: ModelDBOType) -> ModelDBOType:
        raise NotImplementedError()
    
    async def get(self, dbo_cls: Type[ModelDBOType], attr: str, value: Any) -> ModelDBOType | None:
        raise NotImplementedError()

    async def get_list(
        self,
        dbo_cls: Type[ModelDBOType],
        attrs: Dict[str, Any] | None = None,
        order_by: str = "id",
        order_direction: str = "desc",
        limit: int = 100,
        offset: int = 0,
    ) -> list[ModelDBOType]:
        raise NotImplementedError()
    
    async def delete(self, dbo: ModelDBOType) -> None:
        raise NotImplementedError()
    
    async def get_count(self, dbo_cls: Type[ModelDBOType], attrs: Dict[str, Any] | None = None) -> int:
        raise NotImplementedError()
