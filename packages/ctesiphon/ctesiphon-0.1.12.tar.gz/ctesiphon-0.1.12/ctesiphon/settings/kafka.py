from pydantic import BaseModel


class KafkaSettings(BaseModel):
    bootstrap: str = ""
    metric_bootstrap: str = ""
