from typing import TypedDict


class UserData(TypedDict):
    user_id: str
    username: str
    email: str
    password: str
    is_mfa_enabled: bool

