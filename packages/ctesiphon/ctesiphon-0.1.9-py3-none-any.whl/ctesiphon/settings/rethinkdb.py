from pydantic import BaseModel, AnyUrl


class RethinkDBSettings(BaseModel):
    dsn: AnyUrl
