from fastapi import Depends, UploadFile, File, APIRouter

from signature_detector.domain import SignatureDetectingHandler
from .application import get_detecting_handler
from .schemas import ResponseModel

router = APIRouter(prefix='/v1/signature_detector')

__all__ = ('router',)


@router.post('/detect_signature', response_model=ResponseModel)
async def detect_signature(file: UploadFile = File(...), handler: SignatureDetectingHandler = Depends(get_detecting_handler)):
    response_data = await handler.handle_image(file.file.read())
    return ResponseModel(data=response_data)
