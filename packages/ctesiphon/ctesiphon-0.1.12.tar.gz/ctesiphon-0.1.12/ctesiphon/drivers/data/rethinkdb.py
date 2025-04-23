from datetime import datetime
from typing import Any, Dict, Type
from uuid import UUID

from rethinkdb import RethinkDB
from rethinkdb.net import Cursor
from ulid import ULID

from .base import BaseDBODriver
from ...dbo import RethinkDBModelDBOType
from ...enums import ConditionTypes
from ...settings import RethinkDBSettings
from ...utils.dt import now
from ...utils.conditions import Condition


class RethinkDBDBODriver(BaseDBODriver):
    def __init__(self, settings: RethinkDBSettings):
        self.settings = settings

        self._rdb = RethinkDB()

    def connect(self):
        return self._rdb.connect(
            host=self.settings.dsn.host,
            port=int(self.settings.dsn.port),
            password=self.settings.dsn.password,
            db=self.settings.dsn.path.replace("/", ""),
        )

    async def create_model(self, dbo_cls: RethinkDBModelDBOType):
        with self.connect() as conn:
            tablename = dbo_cls.__tablename__

            table_list = self._rdb.table_list().run(conn)
            if tablename not in table_list:
                self._rdb.table_create(tablename).run(conn)

    async def init_model(self, dbo_cls: RethinkDBModelDBOType):
        with self.connect() as conn:
            tablename = dbo_cls.__tablename__
            indexes = dbo_cls.__indexes__

            table_list = self._rdb.table_list().run(conn)
            if tablename in table_list:
                indexes_list = self._rdb.table(tablename).index_list().run(conn)
                for index in indexes:
                    if index not in indexes_list:
                        self._rdb.table(tablename).index_create(index).run(conn)
                self._rdb.table(tablename).index_wait().run(conn)

    async def save(self, dbo: RethinkDBModelDBOType, is_new: bool = False):
        with self.connect() as conn:
            if not dbo.id:
                is_new = True
                dbo.id = ULID().to_uuid4()

            if not dbo.created_dt:
                dbo.created_dt = now()
            
            dbo.updated_dt = now()

            if is_new:
                self._rdb.table(dbo.__tablename__).insert(dbo.model_dump(mode="json")).run(conn)
            else:
                self._rdb.table(dbo.__tablename__).get(str(dbo.id)).replace(dbo.model_dump(mode="json")).run(conn)

            return dbo

    def adapt_value(self, value: Any) -> Any:
        if isinstance(value, UUID):
            return str(value)
        else:
            return value
        
    def create_filter(self, attrs: dict):
        def query_filter(row: Any):
            expr = self._rdb.expr(True)
            if attrs and len(attrs.keys()) > 0:
                for key in attrs.keys():
                    if isinstance(attrs[key], Condition):
                        key_value: Condition = attrs[key]
                        if isinstance(key_value.value, datetime):
                            filter_field = self._rdb.iso8601(row[key])
                        else:
                            filter_field = row[key]
                        if key_value.type == ConditionTypes.NOT_EQ:
                            expr = expr & (filter_field != self.adapt_value(key_value.value))
                        elif key_value.type == ConditionTypes.GT:
                            expr = expr & (filter_field > self.adapt_value(key_value.value))
                        elif key_value.type == ConditionTypes.GT_EQ:
                            expr = expr & (filter_field >= self.adapt_value(key_value.value))
                        elif key_value.type == ConditionTypes.LE:
                            expr = expr & (filter_field < self.adapt_value(key_value.value))
                        elif key_value.type == ConditionTypes.LE_EQ:
                            expr = expr & (filter_field <= self.adapt_value(key_value.value))
                        elif key_value.type == ConditionTypes.ONE_OF:
                            expr = expr & (self._rdb.expr(key_value.value).contains(row[key]))
                    elif isinstance(attrs[key], str):
                        expr = expr & (row[key] == attrs[key])
                    else:
                        if isinstance(attrs[key], datetime):
                            filter_field = self._rdb.iso8601(row[key])
                        else:
                            filter_field = row[key]
                        expr = expr & (filter_field == attrs[key])
            return expr
        return query_filter


    async def get(self, dbo_cls: RethinkDBModelDBOType, attr: str, value: Any) -> RethinkDBModelDBOType | None:
        with self.connect() as conn:
            tablename = dbo_cls.__tablename__
            indexes = dbo_cls.__indexes__

            query = self._rdb.table(tablename)
            attr_value = self.adapt_value(value)

            if attr == "id":
                query = query.get(attr_value)
            elif attr in indexes:
                if attr_value is None:
                    return None
                query = query.get_all(attr_value, index = attr)
            else:
                query = query.filter(self._rdb.row[attr] == attr_value)

            result = query.run(conn)

            if isinstance(result, Cursor):
                result_doc = None
                for doc in result:
                    result_doc = doc
                    break
                result = result_doc

            if result is None:
                return result

            return dbo_cls.model_validate(result)
    
    async def get_list(
        self,
        dbo_cls: RethinkDBModelDBOType,
        attrs: Dict[str, Any] | None = None,
        order_by: str = "id",
        order_direction: str = "desc",
        limit: int = 100,
        offset: int = 0,
    ) -> list[RethinkDBModelDBOType]:
        with self.connect() as conn:
            tablename = dbo_cls.__tablename__
            result_items: list[RethinkDBModelDBOType] = []

            query = self._rdb.table(tablename)
            adapt_attrs = {}
            if attrs:
                for key in attrs.keys():
                    adapt_attrs[key] = self.adapt_value(attrs[key])

            query = query.filter(self.create_filter(adapt_attrs))
            if order_direction == "desc":
                query = query.order_by(self._rdb.desc(order_by))
            else:
                query = query.order_by(self._rdb.asc(order_by))
            query = query.skip(offset).limit(limit)

            cursor = query.run(conn)
            for item in list(cursor):
                result_items.append(dbo_cls.model_validate(item))

            return result_items

    async def delete(self, dbo: RethinkDBModelDBOType):
        with self.connect() as conn:
            tablename = dbo.__tablename__

            query = self._rdb.table(tablename)
            query = query.get(str(dbo.id))
            query = query.delete()

            query.run(conn)

    async def get_count(self, dbo_cls: Type[RethinkDBModelDBOType], attrs: Dict[str, Any] | None = None) -> int:
        with self.connect() as conn:
            tablename = dbo_cls.__tablename__

            query = self._rdb.table(tablename)
            if attrs:
                for key in attrs.keys():
                    attrs[key] = self.adapt_value(attrs[key])
                query = query.filter(attrs)
            query = query.count()

            result = query.run(conn)

            return result

    async def rename_table(self, old_name: str, new_name: str):
        result = None

        with self.connect() as conn:
            query = self._rdb.table(old_name).config().update({
                "name": new_name,
            })

            try:
                result = query.run(conn)
                print(f"Success: Rename table: [{old_name}] => [{new_name}]")
            except:
                print(f"Error: Rename table: [{old_name}] => [{new_name}]")
            return result

    async def check_db(self) -> bool:
        result = []

        with self.connect() as conn:
            table_list = self._rdb.table_list().run(conn)
            for table_name in table_list:
                table_status = self._rdb.table(table_name).status().run(conn)
                conditions = [
                    table_status.get("status").get("all_replicas_ready"),
                    table_status.get("status").get("ready_for_outdated_reads"),
                    table_status.get("status").get("ready_for_reads"),
                    table_status.get("status").get("ready_for_writes"),
                ]

                local_result = all(conditions)
                result.append(local_result)

        return all(result)
