import time

from typing import Any, Dict, Type
from uuid import UUID

from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from ulid import ULID

from .base import BaseDBODriver
from ...dbo import ClickhouseModelDBOType
from ...settings import ClickhouseSettings


class ClickhouseDBODriver(BaseDBODriver):
    def __init__(self, settings: ClickhouseSettings):
        self.settings = settings

    async def connect(self) -> AsyncClient:
        return await get_async_client(
            username=self.settings.dsn.username,
            host=self.settings.dsn.host,
            port=int(self.settings.dsn.port),
            password=self.settings.dsn.password,
            database=self.settings.dsn.path.replace("/", ""),
        )
    
    def adapt_value(self, value: Any) -> Any:
        if isinstance(value, UUID):
            return str(value)
        else:
            return value

    async def create_model(self, dbo_cls: ClickhouseModelDBOType):
        client = await self.connect()
        table_list_res = await client.query("SHOW TABLES;")
        table_list = [ item[0] for item in table_list_res.result_rows ]
        if dbo_cls.__tablename__ not in table_list:
            await client.command(dbo_cls.get_create_query())

    async def init_model(self, dbo_cls: ClickhouseModelDBOType):
        pass

    async def rename_model(self, old_name: str, new_name: str):
        try:
            client = await self.connect()
            result = await client.command(f"RENAME TABLE {old_name} TO {new_name};")

            return result
        except:
            return None

    async def get_models_list(self) -> list[str]:
        client = await self.connect()
        res = await client.query("SHOW TABLES;")
        return [ item[0] for item in res.result_rows ]

    async def save(self, dbo: ClickhouseModelDBOType, **extra):
        if dbo.id:
            raise Exception("Clickhouse driver does not support update operations")
        
        dbo.id = ULID().to_uuid4()
        dbo.ts = time.time_ns()

        dbo_data = dbo.model_dump()
        values = [ self.adapt_value(item) for item in list(dbo_data.values()) ]
        client = await self.connect()
        await client.insert(dbo.__tablename__, [values])

        return dbo

    async def get(self, dbo_cls: ClickhouseModelDBOType, attr: str, value: Any) -> ClickhouseModelDBOType | None:
        request = f"select * from {dbo_cls.__tablename__} where {attr} = '{value}' limit 1;"

        client = await self.connect()
        res = await client.query(request)

        if len(res.result_rows) < 1:
            return None
        
        res = res.result_rows[0]

        res_data = {}
        for i in range(len(res)):
            value = res[i]
            key = dbo_cls.get_fields()[i]
            res_data[key] = value

        return dbo_cls.model_validate(res_data)

    async def get_list(
        self,
        dbo_cls: ClickhouseModelDBOType,
        attrs: Dict[str, Any] | None = None,
        order_by: str = "id",
        order_direction: str = "desc",
        limit: int = 100,
        offset: int = 0,
    ) -> list[ClickhouseModelDBOType]:
        if order_by not in dbo_cls.get_fields():
            order_by = "id"

        conditions = []
        for key, attr in attrs.items():
            conditions.append(f"{key} = '{attr}'")

        request = f"select * from {dbo_cls.__tablename__} where {' and '.join(conditions)} order by {order_by} {order_direction} limit {limit};"
        result = await self.query(dbo_cls, request)
        return result

    async def delete(self, dbo: ClickhouseModelDBOType):
        raise Exception("Clickhouse driver does not support delete operations")

    async def get_count(
        self,
        dbo_cls: Type[ClickhouseModelDBOType],
        attrs: Dict[str, Any] | None = None
    ) -> int:
        conditions = []
        for key, attr in attrs.items():
            conditions.append(f"{key} = '{attr}'")

        request = f"select count() from {dbo_cls.__tablename__} where {' and '.join(conditions)};"
        client = await self.connect()
        res = await client.query(request)
        return int(res.result_rows[0][0])

    async def raw_execute(self, request: str): # pragma: no cover
        client = await self.connect()
        await client.command(request)

    async def raw_query(self, request: str) -> list[ClickhouseModelDBOType]: # pragma: no cover
        client = await self.connect()
        return await client.query(request)
    
    async def query(self, dbo_cls: ClickhouseModelDBOType, request: str) -> list[ClickhouseModelDBOType]:
        result = []

        client = await self.connect()
        res = await client.query(request)

        for row in res.result_rows:
            row_data = {}
            for i in range(len(row)):
                value = row[i]
                key = dbo_cls.get_fields()[i]
                row_data[key] = value
            result.append(dbo_cls.model_validate(row_data))

        return result
