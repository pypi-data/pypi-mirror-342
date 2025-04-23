from pydantic import BaseModel


class CommunicationsSettings(BaseModel):
    email_actions_topic: str = "email_actions"
    email_sender: str | None = None

    smtp_host: str | None = None
    smtp_port: str | None = None
    smtp_username: str | None = None
    smtp_password: str | None = None
