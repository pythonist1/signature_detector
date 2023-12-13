import pytest
from signature_detector.bootstrap import bootstrap_database_engine
from signature_detector.storage.table import metadata


@pytest.fixture
def get_engine():
    async def engine_factory():
        async_engine = bootstrap_database_engine()
        async with async_engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)
        return async_engine
    return engine_factory