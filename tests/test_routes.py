import pytest

def test_fetch_rates_success_portCode(client):
    # Test for successful retrieval of rates using port codes
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination=IEDUB"
    )
    assert response.status_code == 200

def test_fetch_rates_success_slug(client):
    # Test for successful retrieval of rates using slugs
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-02&origin=china_main&destination=north_europe_main"
    )
    assert response.status_code == 200

def test_fetch_rates_success_region(client):
    # Test for successful retrieval of rates using region names
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-02&origin=china_main&destination=northern_europe"
    )
    assert response.status_code == 200

def test_fetch_rates_invalid_date_format(client):
    # Test for invalid date format in request parameters
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=20170111&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Invalid date format" in data["error"]

def test_fetch_rates_missing_parameters_date_to(client):
    # Test for missing 'date_to' parameter in request
    response = client.get(
        "/rates?date_from=2024-01-01&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    # Test for missing 'date_to' parameter value in request
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_missing_parameters_date_from(client):
    # Test for missing 'date_from' parameter in request
    response = client.get(
        "/rates?date_to=2017-01-11&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    # Test for missing 'date_from' parameter value in request
    response = client.get(
        "/rates?date_from=&date_to=2017-01-11&origin=CNSGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_missing_parameters_origin(client):
    # Test for missing 'origin' parameter in request
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    # Test for missing 'origin' parameter value in request
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_missing_parameters_destination(client):
    # Test for missing 'destination' parameter in request
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

    # Test for missing 'destination' parameter value in request
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination="
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing" in data["error"]

def test_fetch_rates_with_invalid_origin_port_code(client):
    """
    Test handling of invalid origin port code in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=C@SGH&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Port C@SGH does not exist." in data["error"]

def test_fetch_rates_with_invalid_destination_port_code(client):
    """
    Test handling of invalid destination port code in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination=I@DUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Port I@DUB does not exist." in data["error"]

def test_fetch_rates_with_invalid_origin_slug(client):
    """
    Test handling of invalid origin slug in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=invalid_slug&destination=IEDUB"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Region invalid_slug does not exist." in data["error"]

def test_fetch_rates_with_invalid_destination_slug(client):
    """
    Test handling of invalid destination slug in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination=invalid_slug"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Region invalid_slug does not exist." in data["error"]

def test_fetch_rates_with_non_existent_region_and_port(client):
    """
    Test handling of non-existent region and port code in request.
    """
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2017-01-11&origin=nonexistent&destination=invalid"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "Region nonexistent does not exist." in data["error"]

def test_fetch_rates_missing_all_parameters(client):
    """
    Test handling of missing required parameters: date_from, date_to, origin, and destination.
    """
    response = client.get("/rates")
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing: date_from, date_to, origin, destination" in data["error"]

def test_fetch_rates_missing_date_to_origin_and_destination(client):
    """
    Test handling of missing required parameters: date_to, origin, and destination when date_from is provided.
    """
    response = client.get("rates?date_from=2016-01-01")
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing: date_to, origin, destination" in data["error"]

def test_fetch_rates_missing_origin_and_destination(client):
    """
    Test handling of missing required parameters: origin and destination when date_from and date_to are provided.
    """
    response = client.get("/rates?date_from=2016-01-10&date_to=2017-01-11")
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing: origin, destination" in data["error"]

def test_fetch_rates_missing_destination(client):
    """
    Test handling of missing required parameter: destination when date_from and date_to and origin are provided.
    """
    response = client.get("/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNGGZ")
    data = response.get_json()
    assert response.status_code == 400
    assert "Required parameter(s) missing: destination" in data["error"]