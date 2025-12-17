from .mortgage_math import monthly_mortgage_payment

def calculate_affordability(
    income,
    down_payment,
    interest_rate,
    loan_term,
    property_tax=None,
    home_insurance=None,
    hoa=None,
    include_mi=False,
    mi_amount=None,
):
    monthly_income = income / 12
    max_housing_ratio = 0.25
    max_monthly_payment = monthly_income * max_housing_ratio

    r = (interest_rate / 100) / 12
    n = loan_term * 12

    tax_rate = (property_tax / 100) if property_tax else 0
    ins_rate = (home_insurance / 100) if home_insurance else 0
    mi_rate  = (mi_amount / 100) if (include_mi and mi_amount) else 0

    home_value = 200000.0

    for _ in range(8):
        mortgage_amount = home_value - down_payment

        if include_mi and mortgage_amount / home_value > 0.80:
            annual_mi = mortgage_amount * mi_rate
            monthly_mi = annual_mi / 12
        else:
            monthly_mi = 0

        monthly_tax = (home_value * tax_rate) / 12
        monthly_ins = (home_value * ins_rate) / 12
        monthly_hoa = hoa if hoa else 0

        non_principal_costs = (
            monthly_tax +
            monthly_ins +
            monthly_hoa +
            monthly_mi
        )

        mortgage_payment_allowed = max_monthly_payment - non_principal_costs
        mortgage_payment_allowed = max(mortgage_payment_allowed, 0)

        if r > 0:
            factor = round((1 - (1 + r) ** -n) / r, 8)
            mortgage_amount = mortgage_payment_allowed * factor
        else:
            mortgage_amount = mortgage_payment_allowed * n

        home_value = mortgage_amount + down_payment

    return {
        "down_payment_pct": (down_payment / home_value) * 100 if home_value > 0 else 0,
        "monthly_payment": max_monthly_payment,
        "income_pct": (max_monthly_payment / monthly_income) * 100,
        "home_value": home_value,
    }
