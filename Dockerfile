FROM python:3.9-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-interaction --no-root

COPY . .
