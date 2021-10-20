# backend
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<a href="https://gitmoji.dev">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji">
</a>

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