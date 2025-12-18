def test_custom_route_post(client):
    response = client.post("/calculators/house-affordability/custom", data={
        "income": "120000",
        "dp_mode": "percent",
        "down_payment_slider": "20",
        "income_pct_slider": "25",
        "interest_rate": "6",
        "loan_term": "30"
    })
    assert response.status_code == 200
    assert b"Estimated Monthly Payment" in response.data
