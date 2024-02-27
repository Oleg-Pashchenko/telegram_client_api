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
            data = await request.read()
            decoded_string = data.decode('utf-8')

            # Parsing the query string into a dictionary
            parsed_data = parse_qs(decoded_string)

            # Since parse_qs keeps values in lists, we can convert them to single values
            data = {k: v[0] for k, v in parsed_data.items()}
            # Преобразуйте байты в строку, если это необходимо
            print(data)
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

