from typing import Type, Generic, Any, Dict

from uuid import UUID as base_uuid_type

from ctesiphon.dbo.base import ModelDBOType
from ctesiphon.drivers.data.base import BaseDBODriver
from ctesiphon.dto.base import ModelDTOType


class ModelRepository(Generic[ModelDTOType, ModelDBOType]): # type: ignore
    def __init__(
        self,
        driver: BaseDBODriver,
    ):
        self.driver = driver

    @property
    def model_dbo(self) -> Type[ModelDBOType]:
        return self.__orig_bases__[0].__args__[1]

    @property
    def model_dto(self) -> Type[ModelDTOType]:
        return self.__orig_bases__[0].__args__[0]

    def dto_to_dbo(self, item: ModelDTOType) -> ModelDBOType:
        item_dict = self.item_to_dict(item)
        return self.model_dbo(**item_dict)

    def dbo_to_dto(self, item: ModelDBOType) -> ModelDTOType:
        item_dict = self.item_to_dict(item)
        return self.model_dto(**item_dict)

    def item_to_dict(self, item: Type[ModelDBOType] | Type[ModelDTOType]) -> dict:
        result = {}

        if item.id is not None:
            result['id'] = item.id

        fields_list_dto = self.model_dto.get_fields()
        fields_list_dbo = self.model_dbo.get_fields()
        fields_list = [ item for item in fields_list_dto if item in fields_list_dbo ]

        for field in fields_list:
            if field not in result:
                result[field] = getattr(item, field)

        return result

    async def init(self):
        await self.driver.init_model(self.model_dbo)

    async def create_model(self):
        await self.driver.create_model(self.model_dbo)

    async def save(self, item: ModelDTOType | dict) -> ModelDTOType:
        if isinstance(item, dict):
            dbo_obj = self.model_dbo(**item)
        else:
            dbo_obj = self.dto_to_dbo(item)
        dbo_obj = await self.driver.save(dbo_obj)

        return self.dbo_to_dto(dbo_obj)

    async def get_by_attr(self, attr: str, value: Any) -> ModelDTOType | None:
        item = await self.driver.get(self.model_dbo, attr, value)
        if not item:
            return None
        return self.dbo_to_dto(item)

    async def get_by_params(
        self,
        attrs: Dict[str, Any] | None = None,
        order_by: str = "id",
        order_direction: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> ModelDTOType | None:
        items_result = await self.driver.get_list(
            self.model_dbo,
            attrs,
            order_by=order_by,
            order_direction=order_direction,
            limit=limit,
            offset=offset,
        )

        if len(items_result) == 0:
            return None

        return self.dbo_to_dto(items_result[0])
    
    async def refresh(self, item: ModelDTOType) -> ModelDTOType | None:
        return await self.get_by_id(item.id)

    async def get_by_id(self, item_id: base_uuid_type | str) -> ModelDTOType | None:
        if isinstance(item_id, base_uuid_type):
            prep_item_id = item_id
        else:
            try:
                prep_item_id = base_uuid_type(item_id)
            except:
                return None

        item = await self.driver.get(self.model_dbo, "id", prep_item_id)
        if not item:
            return None

        return self.dbo_to_dto(item)

    async def get_list_by_attr(
        self,
        attr: str,
        value: Any,
        order_by: str = "created_dt",
        order_direction: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> list[ModelDTOType]:
        return await self.get_list_by_params(
            { attr: value },
            order_by=order_by,
            order_direction=order_direction,
            limit=limit,
            offset=offset,
        )

    async def get_list_by_params(
        self,
        attrs: Dict[str, Any] | None = None,
        order_by: str = "created_dt",
        order_direction: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> list[ModelDTOType]:
        items_result = await self.driver.get_list(
            self.model_dbo,
            attrs,
            order_by=order_by,
            order_direction=order_direction,
            limit=limit,
            offset=offset,
        )

        return [ self.dbo_to_dto(item) for item in items_result ]
    
    async def get_count_by_params(self, attrs: Dict[str, Any] | None = None) -> int:
        return await self.driver.get_count(self.model_dbo, attrs)

    async def delete(self, item: ModelDTOType) -> None:
        dbo_obj = self.dto_to_dbo(item)
        await self.driver.delete(dbo_obj)
