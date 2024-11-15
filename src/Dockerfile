FROM python:3.12-alpine

WORKDIR /usr/app/src

COPY poetry.lock pyproject.toml ./
COPY . /usr/app/src/

RUN pip install poetry --no-cache-dir

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# EXPOSE 8000
#
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]