from pydantic import BaseModel, AnyUrl


class ClickhouseSettings(BaseModel):
    dsn: AnyUrl | None = None
