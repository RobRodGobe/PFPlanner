from Backend.services.house_affordability_custom import solve_max_home_price

def test_custom_solver_basic():
    result = solve_max_home_price(
        income_monthly=10000,
        income_pct_limit=25,
        dp_mode="percent",
        dp_slider=20,
        dp_max_dollar=0,
        interest_rate=6,
        loan_term=30,
        property_tax=1,
        home_insurance=1,
        hoa=0,
        mi_pct=0
    )
    assert "home_value" in result
    assert "monthly_payment" in result
    assert "allowed_payment" in result
    assert "down_payment" in result
    assert round(result["monthly_payment"]) == 2500  # example
    assert round(result["home_value"]) == 386813  # example
