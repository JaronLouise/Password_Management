from typing import TypedDict


class UserData(TypedDict):
    user_id: str
    username: str
    password: str
    is_mfa_enabled: bool
    mfa_auth: dict


class MfaData(TypedDict):
    email: str
    contact_number: str
