import aiohttp_cors

from src.router import web, app


if __name__ == '__main__':
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    for route in list(app.router.routes()):
        print(route)
        cors.add(route)

    web.run_app(app, host='0.0.0.0', port=5003)
