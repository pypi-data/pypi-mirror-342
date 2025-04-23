from typing import TypeVar, Union, Annotated, get_origin, get_args
from uuid import UUID

from pydantic import UUID4
from pydantic.types import UuidVersion
from ulid import ULID

from .base import BaseDBO


class ClickhouseBaseDBO(BaseDBO):
    __tablename__: str = "objects"
    __engine__: str = "MergeTree"
    __index_granularity__: int = 8192

    id: UUID4 | None = None
    ts: int = -1

    @classmethod
    def get_fields(cls) -> list[str]:
        return [ field_name for field_name, _ in cls.model_fields.items() ]
    
    @classmethod
    def get_create_query(cls) -> str:
        fields = [
            "`id` UUID",
            "`ts` UInt64",
        ]

        for field_name, field_info in cls.model_fields.items():
            if field_name not in ["id", "ts"]:
                is_optional = False
                field_type = "String"
                annotation_args = get_args(field_info.annotation)
                annotation_origin = get_origin(field_info.annotation)

                if annotation_origin == Union:
                    for annotation_arg in annotation_args:
                        if annotation_arg == None.__class__:
                            is_optional = True
                        else:
                            if get_origin(annotation_arg) == Annotated:
                                annotated_args = get_args(annotation_arg)
                                if UUID in annotated_args:
                                    field_type = "UUID"

                if field_info.annotation == int:
                    field_type = "Int64"
                elif field_info.annotation == float:
                    field_type = "Float64"
                elif field_info.annotation in [UUID, UUID4, ULID]:
                    field_type = "UUID"

                if is_optional:
                    result_field_type = f"Nullable({field_type})"
                else:
                    result_field_type = field_type

                fields.append(f"`{field_name}` {result_field_type}")

        query = f"""
            CREATE TABLE IF NOT EXISTS {cls.__tablename__}
            ({",".join(fields)})
            ENGINE = {cls.__engine__}
            PRIMARY KEY id
            ORDER BY id
            SETTINGS index_granularity = {cls.__index_granularity__}
            COMMENT 'migration:1';
        """

        return query


ModelDBOType = TypeVar('ModelDBOType', bound=ClickhouseBaseDBO)
