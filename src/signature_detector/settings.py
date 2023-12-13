import pathlib

from pydantic import BaseSettings

from signature_detector.domain import SignatureDetectingHandler

__all__ = ('config',)


project_path = pathlib.Path(__file__).parent
env_path = str(project_path) + '/.env'


class Config(BaseSettings):
    postgres_url: str
    gateway_app_host: str = '0.0.0.0'
    gateway_app_port: int = 8000
    detecting_handler: SignatureDetectingHandler = None


config = Config(_env_file=env_path)
