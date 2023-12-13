import logging

from fastapi import FastAPI, APIRouter, Request
from starlette.responses import JSONResponse

from signature_detector.settings import Config


async def base_exception_handler(app, request: Request, exc: Exception):
    logging.getLogger('gateway').error('Internal service error', exc_info=exc, extra={'path': request.url.path})
    return JSONResponse(
        status_code=200,
        content={
            'status': "ERROR",
            'data': {},
            'exc_code': 'InternalServiceError',
            'exc_data': {},
            'message': repr(exc),
        }
    )


def get_detecting_handler():
    from signature_detector.bootstrap import config
    return config.detecting_handler


class ApplicationConfig:
    BASE_EXCEPTION_HANDLER = base_exception_handler

    def __init__(self, config: Config):
        self._routers = list()
        self.host = config.gateway_app_host
        self.port = config.gateway_app_port

    def include_router(self, router: APIRouter):
        self._routers.append(router)

    def get_application(self) -> FastAPI:
        app = FastAPI()

        app.add_exception_handler(Exception, self.BASE_EXCEPTION_HANDLER)

        for router in self._routers:
            app.include_router(router)

        return app
