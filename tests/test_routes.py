import pytest

def test_fetch_rates_with_valid_port_codes(client):
    """
    Test successful retrieval of rates using valid port codes.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination=IEDUB"
    )
    assert response.status_code == 200

def test_fetch_rates_with_valid_slugs(client):
    """
    Test successful retrieval of rates using valid slugs.
    """
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-02&origin=china_main&destination=north_europe_main"
    )
    assert response.status_code == 200

def test_fetch_rates_with_valid_region_names(client):
    """
    Test successful retrieval of rates using valid region names.
    """
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-02&origin=china_main&destination=northern_europe"
    )
    assert response.status_code == 200

def test_fetch_rates_with_invalid_date_format(client):
    """
    Test handling of invalid date format in request parameters.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=20170111&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Invalid date format" in data["error"]

def test_fetch_rates_with_missing_date_to(client):
    """
    Test handling of missing 'date_to' parameter in request.
    """
    response = client.get(
        "/rates?date_from=2024-01-01&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    response = client.get(
        "/rates?date_from=2016-01-10&date_to=&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_with_missing_date_from(client):
    """
    Test handling of missing 'date_from' parameter in request.
    """
    response = client.get(
        "/rates?date_to=2017-01-11&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    response = client.get(
        "/rates?date_from=&date_to=2017-01-11&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_with_missing_origin(client):
    """
    Test handling of missing 'origin' parameter in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_with_missing_destination(client):
    """
    Test handling of missing 'destination' parameter in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination="
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]
