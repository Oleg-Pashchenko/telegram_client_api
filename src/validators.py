from pydantic import BaseModel


class TelegramCodeData(BaseModel):
    api_id: int
    api_hash: str
    phone: str


class AuthData(BaseModel):
    session_name: str
    sms_code: str


class AuthWith2FAData(BaseModel):
    session_name: str
    secret_password: str


class GetUpdatesData(BaseModel):
    session_name: str
