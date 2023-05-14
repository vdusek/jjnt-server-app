# Jak jsme na tom? - Server app

## Description

- Server application (backend, REST API) of [Jak jsme na tom?](https://jakjsmenatom.cz/) project.
- Implemented in Python utilizing [FastAPI](https://fastapi.tiangolo.com).

## API endpoints

### [Swagger](https://swagger.io/) docs

- [localhost:8000/docs](http://localhost:8000/docs)

### Local

- [localhost:8000/indicators](http://localhost:8000/indicators/)
- [localhost:8000/categories](http://localhost:8000/categories/)
- [localhost:8000/indicators/wb/hdp](http://localhost:8000/indicators/wb/hdp/)
- [localhost:8000/sources/imf/hdp_na_obyvatele](http://localhost:8000/sources/imf/hdp_na_obyvatele/)
- [localhost:8000/options/charts](http://localhost:8000/options/charts/)
- [localhost:8000/options/groups](http://localhost:8000/options/groups/)
- [localhost:8000/options/sources/hdp](http://localhost:8000/options/sources/hdp/)
- [localhost:8000/options/years/wb/hdp/v4](http://localhost:8000/options/years/wb/hdp/v4/)
- [localhost:8000/data/tabulka/wb/hdp/eu/2020](http://localhost:8000/data/tabulka/wb/hdp/eu/2020/)
- [localhost:8000/data/tabulka/wb/hdp/eu/posledni_znamy](http://localhost:8000/data/tabulka/wb/hdp/eu/posledni_znamy/)
- [localhost:8000/data/mapa/wb/hdp/eu/2020](http://localhost:8000/data/mapa/wb/hdp/eu/2020/)
- [localhost:8000/data/mapa/wb/hdp/eu/posledni_znamy](http://localhost:8000/data/mapa/wb/hdp/eu/posledni_znamy/)
- [localhost:8000/data/sloupcovy_graf/wb/hdp/eu/2020](http://localhost:8000/data/sloupcovy_graf/wb/hdp/eu/2020/)
- [localhost:8000/data/sloupcovy_graf/wb/hdp/eu/posledni_znamy](http://localhost:8000/data/sloupcovy_graf/wb/hdp/eu/posledni_znamy/)
- [localhost:8000/data/kolacovy_graf/wb/hdp/eu/2020](http://localhost:8000/data/kolacovy_graf/wb/hdp/eu/2020/)
- [localhost:8000/data/kolacovy_graf/wb/hdp/eu/posledni_znamy](http://localhost:8000/data/kolacovy_graf/wb/hdp/eu/posledni_znamy/)
- [localhost:8000/data/liniovy_graf/wb/hdp/eu/2015/2020](http://localhost:8000/data/liniovy_graf/wb/hdp/eu/2015/2020/)
- [localhost:8000/data/liniovy_graf/wb/hdp/eu/2015/posledni_znamy](http://localhost:8000/data/liniovy_graf/wb/hdp/eu/2015/posledni_znamy/)

## Development setup

- [Poetry](https://python-poetry.org/) project.

Install dependencies

```
poetry install
```

Activate current virtual env

```
poetry shell
```

Add dependency

```
poetry add [--group dev] pypi_package
```

Run pytest

```
poetry run pytest --verbose --cov
```

Run pylint

```
poetry run pylint jjnt_api/ tests/
```

Run flake8

```
poetry run flake8 jjnt_api/ tests/
```

Run mypy

```
poetry run mypy .
```

Run black

```
poetry run black .
```

Run isort

```
poetry run isort .
```

### Run a development instance

Using Poetry and Uvicorn

```
poetry run dev
```

### Run a production instance

Using Docker and Docker Compose

```
docker build --tag jjnt-server-app ./
```

```
docker-compose up --detach
```
