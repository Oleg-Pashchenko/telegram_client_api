from src.decorators import request_processing
from src.validators import TelegramCodeData, AuthData, AuthWith2FAData, GetUpdatesData
from src.api import client


@request_processing
async def send_telegram_code_handler(data: dict):
    print(data)
    data = TelegramCodeData(**data)
    print(data)
    return await client.send_telegram_code(data)


@request_processing
async def auth_handler(data: dict):
    data = AuthData(**data)
    return await client.try_auth(data)


@request_processing
async def auth_with_2fa_handler(data: dict):
    data = AuthWith2FAData(**data)
    print(data)
    return await client.try_auth_with_2fa(data)


@request_processing
async def get_updates(data: dict):
    data = GetUpdatesData(**data)
    return await client.get_updates(data)

