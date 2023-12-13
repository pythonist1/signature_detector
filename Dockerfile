FROM mwalbeck/python-poetry:1.2-3.10 as builder

WORKDIR /app

RUN python -m venv .venv

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY src/ ./src

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN poetry install --only main
RUN poetry build
RUN /app/.venv/bin/pip install /app/dist/*.tar.gz && /app/.venv/bin/pip check
RUN ln -snf /app/.venv/bin/run_api /usr/local/bin/

CMD ["run_api"]