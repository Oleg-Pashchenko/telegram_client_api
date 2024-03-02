import os
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
    return {'session_name': session_name}


async def try_auth(data: AuthData):
    tg: Tg = get_tg_entity(data.session_name)
    await tg.connect()
    if data.sms_code.isdigit():
        response = await tg.authorize_by_sms(data.sms_code)
    else:
        response = await tg.authorize_by_password(data.sms_code)
    save_tg_entity(tg)


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

    if not response:
        raise AuthorizationError("Некорректный пароль от 2FA или SMS Code!")
    return response


async def get_updates(data: GetUpdatesData):
    tg: Tg = get_tg_entity(data.session_name)
    try:
        print(tg.phone, tg.secret_password)
      #   try:
      #      if tg.secret_password:
     #           await tg.client.start(phone=tg.phone, password=tg.secret_password)
      #      else:
      #          await tg.client.start(phone=tg.phone)

        me = await tg.client.get_me()
        print(me)
        response = await tg.get_updates()
        print(response)
        save_tg_entity(tg)
    except Exception as e:
        print(e)
        raise Exception("Ошибки случаются. Попробуй перезайти.")
    finally:
        pass
    return response
