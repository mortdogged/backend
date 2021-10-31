# backend
[![codecov](https://codecov.io/gh/mortdogged/backend/branch/main/graph/badge.svg?token=NYKUYQR8ZG)](https://codecov.io/gh/mortdogged/backend)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<a href="https://gitmoji.dev">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji">
</a>

![architecture](./docs/architecture.png)

### Installation
```bash
poetry install
poetry run pre-commit install
```

### Test
```bash
poetry run pytest --cov=app --cov-fail-under=80 --cov-report xml
```

### Run
Fill the `.env` file and run:
```
docker-compose up --build
```
