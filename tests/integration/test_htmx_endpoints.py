def test_custom_advanced_htmx(client):
    response = client.get(
        "/calculators/house-affordability/custom/advanced?show=1",
        headers={"HX-Request": "true"}
    )
    assert response.status_code == 200
    assert b"Advanced" in response.data or b"property" in response.data
