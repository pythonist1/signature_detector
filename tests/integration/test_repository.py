import pytest
import pathlib
from sqlalchemy import text
from datetime import datetime
from signature_detector.bootstrap import bootstrap_handler


path = pathlib.Path(__file__).parent


@pytest.mark.asyncio
async def test_add_result(get_engine):
    engine = await get_engine()
    handler = bootstrap_handler(engine)


    file_path = pathlib.Path.joinpath(path, 'img.png')
    with open(file_path, 'rb') as fp:
        im_b = fp.read()

    response = await handler.handle_image(image_bytes=im_b)

    select_stmt = text('''
        SELECT *
        FROM signature_detecting_result
    ''')

    async with engine.begin() as connection:
        result = (await connection.execute(select_stmt)).first()

    result_dict = result._mapping
    assert result_dict['reference'] == '98fa38592e422c46caf1cc9f498b9b704bc448b685c23b7b0b22d0fbf684575a'
    assert result_dict['is_detected'] == True
    assert  result_dict['detected_quantity'] == 9
    assert isinstance(result_dict['request_time'], datetime)

    assert result_dict['reference'] == response['reference']
    assert result_dict['is_detected'] == response['is_detected']
    assert  result_dict['detected_quantity'] == response['detected_quantity']

    await engine.dispose()
