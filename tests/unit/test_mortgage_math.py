from Backend.services.mortgage_math import monthly_mortgage_payment

def test_zero_interest():
    assert monthly_mortgage_payment(120000, 0, 30) == 120000 / (30 * 12)

def test_positive_interest():
    result = monthly_mortgage_payment(300000, 6, 30)
    assert result > 0
