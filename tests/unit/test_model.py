from signature_detector.domain.model import SignatureDetectingResult
import pathlib

path = pathlib.Path(__file__).parent

def test_init_model():
    file_path = pathlib.Path.joinpath(path, 'img.png')
    with open(file_path, 'rb') as fp:
        im_b = fp.read()
    result = SignatureDetectingResult(
        image_bytes=im_b,
        detected_quantity=9
    )

    assert result.is_detected == True
    assert result.detected_quantity == 9
    assert result.reference == '98fa38592e422c46caf1cc9f498b9b704bc448b685c23b7b0b22d0fbf684575a'
