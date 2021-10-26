FROM python:3.9-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# https://cryptography.io/en/latest/installation/#debian-ubuntu
RUN apt-get install build-essential libssl-dev libffi-dev \
    python3-dev cargo

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-interaction --no-root

COPY . .
