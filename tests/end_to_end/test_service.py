import pathlib
from sqlalchemy import text

path = pathlib.Path(__file__).parent
file_path = pathlib.Path.joinpath(path, 'img.png')


async def test_service(service_test_client):
    engine = service_test_client._engine
    with open(file_path, 'rb') as fp:
        im_b = fp.read()

    status, response_data = await service_test_client.request(
        '/v1/signature_detector/detect_signature',
        file=im_b
    )

    response = response_data['data']

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

    assert result_dict['reference'] == response['reference']
    assert result_dict['is_detected'] == response['is_detected']
    assert  result_dict['detected_quantity'] == response['detected_quantity']

    await engine.dispose()
