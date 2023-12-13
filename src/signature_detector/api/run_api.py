import uvicorn
from signature_detector.bootstrap import bootstrap_gateway, bootstrap_database_engine, bootstrap_handler


def run():
    engine = bootstrap_database_engine()
    bootstrap_handler(engine)
    app_config = bootstrap_gateway()
    app = app_config.get_application()
    uvicorn.run(app, host=app_config.host, port=app_config.port)


if __name__ == '__main__':
    run()
