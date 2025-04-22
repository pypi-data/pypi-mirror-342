from pydantic import BaseModel


class UsersSettings(BaseModel):
    debug_admin_password: str | None = None
    auth_token_length: int = 32
    auth_access_token_expire: int = 7*24*60*60

    auth_magic_link_token_length: int = 16
    auth_magic_link_token_ttl: int = 30

    user_account_id_alphabet: str = "ABCDEFGHJKLMNPRTUVWXYZ0123456789"
    user_account_id_length: int = 10
