from typing import Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: str = 'SUCCESS'
    data: dict = dict()
    exc_code: Optional[str] = None
    exc_data: Optional[str] = None
    message: Optional[str] = None
