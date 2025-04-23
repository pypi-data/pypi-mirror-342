import uuid

from datetime import datetime
from typing import TypeVar, Annotated, Any

from pydantic import (
    BaseModel,
    UUID4,
    AfterValidator,
    Field,
)


class DTO(BaseModel):
    @classmethod
    def get_fields(cls) -> list[str]:
        return [ field_name for field_name, _ in cls.model_fields.items() ]

class BaseDTO(DTO):
    id: None | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))] = Field(
        default=None,
        examples=["00000000-0000-0000-0000-000000000000"],
    )
    created_dt: datetime | None = None
    updated_dt: datetime | None = None


class MetricBaseDTO(DTO):
    id: None | UUID4 | Annotated[str, AfterValidator(lambda x: uuid.UUID(x, version=4))] = Field(default=None)
    ts: int = -1


class BaseEvent(BaseModel):
    event_type: str


class BaseError(Exception):
    http_status: int
    error_code: str
    description: str


class BaseMetric(BaseModel):
    ts: int = 0
    metric_domain: str
    metric: str
    instance: str | None = None
    value: Any


ModelDTOType = TypeVar('ModelDTOType', bound=BaseDTO)
ModelEventType = TypeVar('ModelEventType', bound=BaseEvent)
