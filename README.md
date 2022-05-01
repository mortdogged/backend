# backend
[![codecov](https://codecov.io/gh/mortdogged/backend/branch/main/graph/badge.svg?token=NYKUYQR8ZG)](https://codecov.io/gh/mortdogged/backend)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<a href="https://gitmoji.dev">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji">
</a>

> mortdogged.com isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

![architecture](./docs/architecture.png)

### Installation
```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Test
```bash
pytest --cov=app --cov-fail-under=80 --cov-report xml
```

### Run
Fill the `.env` file and run:
```
python main.py
```

### Build pip-tools
```
pip-compile requirements-dev.in
```
