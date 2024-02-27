import aiohttp_cors

from src.router import web, app

if __name__ == '__main__':
    cors = aiohttp_cors.setup(app)
    for route in list(app.router.routes()):
        cors.add(route, {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

    web.run_app(app, host='0.0.0.0', port=5003)
