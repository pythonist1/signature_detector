from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from signature_detector.domain import SignatureDetectingHandler
from signature_detector.adapter import WordDetectorAdapter
from signature_detector.storage import Repository
from signature_detector.gateway import ApplicationConfig, router
from .settings import config


def bootstrap_database_engine() -> AsyncEngine:
    return create_async_engine(config.postgres_url)


def bootstrap_handler(engine: AsyncEngine):
    adapter = WordDetectorAdapter()
    repository = Repository(engine)
    handler = SignatureDetectingHandler(adapter, repository)
    config.detecting_handler = handler
    return handler


def bootstrap_gateway():
    app_config = ApplicationConfig(config)
    app_config.include_router(router)
    return app_config
