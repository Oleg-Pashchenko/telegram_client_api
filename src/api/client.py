import random

from src.api.core import Tg
from src.api.database import get_tg_entity, save_tg_entity
from src.api.exceptions import AuthorizationError
from src.validators import TelegramCodeData, AuthData, AuthWith2FAData, GetUpdatesData


async def send_telegram_code(data: TelegramCodeData):
    session_name = str(random.randint(1000000, 10000000))
    tg = Tg(
        api_id=data.api_id,
        api_hash=data.api_hash,
        session_name=session_name,
        phone=data.phone
    )
    await tg.connect()
    await tg.send_auth_code()
    save_tg_entity(tg)
    await tg.client.disconnect()
    return {'session_name': session_name}


async def try_auth(data: AuthData):
    tg: Tg = get_tg_entity(data.session_name)
    await tg.connect()
    response = await tg.authorize_by_sms(data.sms_code)
    save_tg_entity(tg)
    print(response)
    await tg.client.disconnect()

    if not response:
        raise AuthorizationError("Подключена 2FA")
    return response


async def try_auth_with_2fa(data: AuthWith2FAData):
    tg: Tg = get_tg_entity(data.session_name)
    print(tg)
    await tg.connect()
    response = await tg.authorize_by_password(data.secret_password)
    print(response)
    save_tg_entity(tg)
    await tg.client.disconnect()

    if not response:
        raise AuthorizationError("Некорректный пароль от 2FA или SMS Code!")
    return response


async def get_updates(data: GetUpdatesData):
    tg: Tg = get_tg_entity(data.session_name)
    await tg.client.start()
    response = await tg.get_updates()
    save_tg_entity(tg)
    await tg.client.disconnect()
    return response
