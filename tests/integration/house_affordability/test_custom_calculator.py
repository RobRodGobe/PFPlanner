import pytest

@pytest.mark.integration
def test_custom_route_status(client):
    response = client.post("calculators/house-affordability/custom", data={
        "income": "120000",
        "down_payment_slider": "20",
        "down_payment_max": "200000",
        "dp_mode": "dollar",
        "income_pct_slider": "25",
        "interest_rate": "6.5",
        "loan_term": "30",
        "custom_advanced_state": "0",
    })
    assert response.status_code == 200


@pytest.mark.integration
def test_custom_renders_results(client):
    response = client.post("calculators/house-affordability/custom", data={
        "income": "120000",
        "down_payment_slider": "20",
        "down_payment_max": "200000",
        "dp_mode": "dollar",
        "income_pct_slider": "25",
        "interest_rate": "6.5",
        "loan_term": "30",
        "custom_advanced_state": "0",
    })
    html = response.get_data(as_text=True)

    assert "Monthly Payment" in html
    assert "$" in html


@pytest.mark.integration
def test_custom_missing_income(client):
    response = client.post("calculators/house-affordability/custom", data={
        "income": "",
        "down_payment_slider": "20",
        "down_payment_max": "200000",
        "dp_mode": "dollar",
        "income_pct_slider": "25",
        "interest_rate": "6.5",
        "loan_term": "30",
        "custom_advanced_state": "0",
    })
    html = response.get_data(as_text=True)

    # Custom calculator does NOT validate income — result will be 0
    # So we assert the template renders, not an error
    assert "Monthly Payment" in html


@pytest.mark.integration
def test_custom_htmx_partial(client):
    response = client.post(
        "calculators/house-affordability/custom",
        data={
            "income": "100000",
            "down_payment_slider": "20",
            "down_payment_max": "200000",
            "dp_mode": "dollar",
            "income_pct_slider": "25",
            "interest_rate": "6.5",
            "loan_term": "30",
            "custom_advanced_state": "0",
        },
        headers={"HX-Request": "true"},
    )

    html = response.get_data(as_text=True)

    assert "<html" not in html.lower()
    assert "<div" in html


@pytest.mark.integration
def test_custom_advanced_fields_htmx(client):
    response = client.get(
        "calculators/house-affordability/custom/advanced",
        query_string={"show": "1"},
        headers={"HX-Request": "true"},
    )

    html = response.get_data(as_text=True)

    assert "Property Tax" in html
    assert "Home Insurance" in html
    assert "HOA" in html
