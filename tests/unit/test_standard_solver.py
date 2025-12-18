from Backend.services.house_affordability_standard import calculate_affordability

def test_standard_solver_math():
    result = calculate_affordability(
        income=120000,
        down_payment=20000,
        interest_rate=6.5,
        loan_term=30,
        property_tax=0,
        home_insurance=0,
        hoa=0,
        include_mi=False,
        mi_amount=0,
    )

    assert round(result["monthly_payment"]) == 2500  # example
    assert round(result["home_value"]) == 415527  # example
