import hashlib
from datetime import datetime


class SignatureDetectingResult:
    def __init__(self, image_bytes: bytes, detected_quantity: int):
        self._is_detected = bool(detected_quantity)
        self._detected_quantity = detected_quantity
        self._reference = hashlib.sha256(image_bytes).hexdigest()
        self._request_time = datetime.now()

    @property
    def is_detected(self):
        return self._is_detected

    @property
    def detected_quantity(self):
        return self._detected_quantity

    @property
    def reference(self):
        return self._reference
