import asyncio

from aiohttp import web

from src.methods import *

app = web.Application()


async def routers():
    app.router.add_post('/send-telegram-code/', await send_telegram_code_handler)
    app.router.add_post('/auth/', await auth_handler)
    app.router.add_post('/auth-with-2fa/', await auth_with_2fa_handler)
    app.router.add_post('/get-updates/', await get_updates)


asyncio.run(routers())
