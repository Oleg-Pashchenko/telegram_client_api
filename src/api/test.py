import asyncio
import datetime
import random

import telethon
from telethon import TelegramClient
from telethon.tl.types import MessageActionGroupCall

api_id = 2724818
api_hash = '6c677b0f0e2af14a53cbf0c0eafe5886'
session_name = str(random.randint(1000000, 10000000))
session_name = '1'
phone = '89870739395'

async def main():
    tg = Tg(
        api_id=api_id,
        api_hash=api_hash,
        session_name=session_name,
        phone=phone
    )
    await tg.connect()
    connection_status = await tg.is_connection_alive()
    if connection_status:
        await tg.get_updates()
        print('yes')
    else:
        print('no')
        await tg.send_auth_code()
        telegram_code = input('Код из телеграма: ')
        await tg.authorize(code=telegram_code)
        two_step_password = 'gelo23122003A!'
        await tg.authorize(code=telegram_code, two_step_password=two_step_password)


asyncio.run(main())
