from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.dialects.postgresql import insert

from signature_detector.domain import AbstractRepository, SignatureDetectingResult
from .table import SignatureDetectingResult as table


class Repository(AbstractRepository):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def add(self, result: SignatureDetectingResult):
        result_data = Converter.convert_result_to_data(result)
        insert_stmt = insert(table).values(result_data)
        async with self._engine.begin() as connection:
            await connection.execute(insert_stmt)
            await connection.commit()


class Converter:
    def convert_result_to_data(result: SignatureDetectingResult):
        result_dict = dict(
            is_detected=result.is_detected,
            detected_quantity=result.detected_quantity,
            reference=result.reference,
            request_time=result._request_time
        )
        return result_dict
