FROM python:3.9-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

COPY ./pyproject.toml ./
RUN echo "[[tool.poetry.source]]" >> ./pyproject.toml && \
    echo 'name = "piwheels"' >> ./pyproject.toml && \
    echo 'url  = "https://www.piwheels.org/simple"' >> ./pyproject.toml \

RUN poetry install --no-interaction --no-root

COPY . .
