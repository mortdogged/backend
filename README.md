# backend

## Develop
Installation
```
poetry install
poetry run pre-commit install
```

Test
```
poetry run pytest --cov=app --cov-fail-under=80 --cov-report xml
```