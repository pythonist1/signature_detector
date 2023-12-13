from signature_detector.domain.use_case import SignatureDetectingHandler
from signature_detector.domain.model import SignatureDetectingResult


class FakeAdapter:
    def detect_signatures(self, image_bytes):
        return 2


result_dict = dict()

class FakeRepository:
    async def add(self, result):
        result_dict['result'] = result


async def test_handle_image(loop):
    handler = SignatureDetectingHandler(
        adapter=FakeAdapter(),
        repository=FakeRepository()
    )
    response = await handler.handle_image(b'image_bytes')

    assert isinstance(result_dict['result'], SignatureDetectingResult)

    assert response['is_detected'] == True
    assert response['detected_quantity'] == 2
    assert response['reference'] == 'd0066f08852f8e7791496222e212b960609c146dce1a46e38653ef741452663a'