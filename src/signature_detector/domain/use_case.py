from .abstractions import AbstractWordDetectorAdapter, AbstractRepository
from .model import SignatureDetectingResult


class SignatureDetectingHandler:
    def __init__(self, adapter: AbstractWordDetectorAdapter, repository: AbstractRepository):
        self._adapter = adapter
        self._repository = repository

    async def handle_image(self, image_bytes: bytes) -> dict:
        detected_quantity = self._adapter.detect_signatures(image_bytes)
        result = SignatureDetectingResult(image_bytes=image_bytes, detected_quantity=detected_quantity)
        await self._repository.add(result=result)
        return {
            'is_detected': result.is_detected,
            'detected_quantity': result.detected_quantity,
            'reference': result.reference
        }
