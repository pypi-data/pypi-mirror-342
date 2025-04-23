from pydantic import BaseModel


class FilesSettings(BaseModel):
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_host: str | None = None
    s3_region: str | None = None
    s3_bucket: str | None = None
