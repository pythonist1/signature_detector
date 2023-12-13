import pathlib
from signature_detector.adapter import WordDetectorAdapter

path = pathlib.Path(__file__).parent
file_path = pathlib.Path.joinpath(path, 'img.png')


def test_adapter():
    with open(file_path, 'rb') as fp:
        im_b = fp.read()

    adapter = WordDetectorAdapter()

    result = adapter.detect_signatures(im_b)

    assert result == 9