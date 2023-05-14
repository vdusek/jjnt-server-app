from fastapi.testclient import TestClient

from jjnt_api.main import app

client = TestClient(app)

# Testing data
source_id = "wb"
indicator_id = "hdp"
group_id = "eu"
year_from = "2015"
year_to = "posledni_znamy"


def test_get_root() -> None:
    url = "/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Swagger documentation is available on /docs endpoint."}


def test_get_docs() -> None:
    url = "/docs"
    response = client.get(url)
    assert response.status_code == 200
    assert response.text  # not empty


def test_get_indicators() -> None:
    url = "/indicators/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_categories() -> None:
    url = "/categories/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_indicator_detail() -> None:
    url = f"/indicators/{source_id}/{indicator_id}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_source_detail() -> None:
    url = f"/sources/{source_id}/{indicator_id}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_options_charts() -> None:
    url = "/options/charts/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_options_groups() -> None:
    url = "/options/groups/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_options_sources() -> None:
    url = f"/options/sources/{indicator_id}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_options_years() -> None:
    url = f"/options/years/{source_id}/{indicator_id}/{group_id}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_data_table() -> None:
    url = f"/data/tabulka/{source_id}/{indicator_id}/{group_id}/{year_to}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_data_map() -> None:
    url = f"/data/mapa/{source_id}/{indicator_id}/{group_id}/{year_to}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_data_barchart() -> None:
    url = f"/data/sloupcovy_graf/{source_id}/{indicator_id}/{group_id}/{year_to}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_data_piechart() -> None:
    url = f"/data/kolacovy_graf/{source_id}/{indicator_id}/{group_id}/{year_to}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty


def test_get_data_linechart() -> None:
    url = f"/data/liniovy_graf/{source_id}/{indicator_id}/{group_id}/{year_from}/{year_to}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()  # not empty
