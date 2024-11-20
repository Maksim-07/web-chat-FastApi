FROM python:3.12-alpine

WORKDIR /usr/app/src

COPY poetry.lock pyproject.toml ./
COPY . /usr/app/src/

RUN pip install poetry --no-cache-dir

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-cache --without dev