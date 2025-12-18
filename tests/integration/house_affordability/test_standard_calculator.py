import pytest

@pytest.mark.integration
def test_standard_route_status(client):
    response = client.post("calculators/house-affordability", data={
        "income": "120000",
        "down_payment": "20000",
        "interest_rate": "6.5",
        "loan_term": "30",
        "advanced_state": "0",
    })
    assert response.status_code == 200


@pytest.mark.integration
def test_standard_renders_results(client):
    response = client.post(
        "/calculators/house-affordability",
        data={
            "income": "120000",
            "down_payment": "20000",
            "interest_rate": "6.5",
            "loan_term": "30",
            "advanced_state": "0",
        },
        headers={"HX-Request": "true"},   # ✅ Required
    )

    html = response.get_data(as_text=True)

    assert "Monthly Payment" in html
    assert "$" in html


@pytest.mark.integration
def test_standard_renders_results(client):
    response = client.post(
        "/calculators/house-affordability",
        data={
            "income": "120000",
            "down_payment": "20000",
            "interest_rate": "6.5",
            "loan_term": "30",
            "advanced_state": "0",
        },
        headers={"HX-Request": "true"},   # ✅ Required
    )

    html = response.get_data(as_text=True)

    assert "Monthly Income" in html
    assert "$" in html


@pytest.mark.integration
def test_standard_htmx_partial(client):
    response = client.post(
        "calculators/house-affordability",
        data={
            "income": "100000",
            "down_payment": "20000",
            "interest_rate": "6.5",
            "loan_term": "30",
            "advanced_state": "0",
        },
        headers={"HX-Request": "true"},
    )

    html = response.get_data(as_text=True)

    assert "<html" not in html.lower()
    assert "<div" in html


@pytest.mark.integration
def test_standard_advanced_fields_htmx(client):
    response = client.get(
        "calculators/house-affordability",
        query_string={"show": "1"},
        headers={"HX-Request": "true"},
    )

    html = response.get_data(as_text=True)

    assert "Property Tax" in html
    assert "Home Insurance" in html
    assert "HOA" in html
