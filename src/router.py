import asyncio

from aiohttp import web

from src.methods import *


async def request_logger_middleware(app, handler):
    async def middleware_handler(request):
        print(f"Запрос: {request.method} {request.rel_url}")
        # Для более детальной информации можно добавить:
        print(f"Заголовки: {request.headers}")
        print(f"Тело запроса: {await request.text()}")
        response = await handler(request)
        return response

    return middleware_handler


app = web.Application(middlewares=[request_logger_middleware])


async def routers():
    app.router.add_post('/send-telegram-code/', await send_telegram_code_handler)
    app.router.add_post('/auth/', await auth_handler)
    app.router.add_post('/auth-with-2fa/', await auth_with_2fa_handler)
    app.router.add_post('/get-updates/', await get_updates)


asyncio.run(routers())
