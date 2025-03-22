from typing import TypedDict


class UserData(TypedDict):
    user_id: str
    username: str
    password: str
    email: str
    is_mfa_enabled: bool
