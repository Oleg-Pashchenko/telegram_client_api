import json
import time
from functools import wraps
from urllib.parse import parse_qs

from aiohttp import web
from src.api.database import get_tg_entity, save_tg_entity


async def request_processing(func):
    @wraps(func)
    async def wrapper(request):
        start_time = time.time()
        print('wrapped')
        try:
            data = json.loads(request.text())

            answer = await func(data)
            status = True
        except Exception as e:
            print(e)
            answer, status = {'error': str(e)}, False

        return web.json_response(
            {
                'status': status,
                'answer': answer,
                'execution_time': round(time.time() - start_time, 2)
            },
            status=200 if status else 500
        )

    return wrapper

