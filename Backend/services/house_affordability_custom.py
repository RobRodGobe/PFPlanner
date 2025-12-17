from .mortgage_math import monthly_mortgage_payment

def solve_max_home_price(
    income_monthly,
    income_pct_limit,
    dp_mode,
    dp_slider,
    dp_max_dollar,
    interest_rate,
    loan_term,
    property_tax,
    home_insurance,
    hoa,
    mi_pct
):
    allowed_payment = income_monthly * (income_pct_limit / 100)

    low, high = 0, 5_000_000

    for _ in range(40):
        P = (low + high) / 2

        # Down payment
        if dp_mode == "percent":
            DP = P * (dp_slider / 100)
        else:
            DP = (dp_slider / 100) * dp_max_dollar

        loan_amount = max(P - DP, 0)

        # Mortgage payment
        M = monthly_mortgage_payment(loan_amount, interest_rate, loan_term)

        # Optional fields
        tax_monthly = P * (property_tax / 100) / 12
        ins_monthly = P * (home_insurance / 100) / 12
        mi_monthly = (loan_amount * (mi_pct / 100)) / 12 if mi_pct else 0

        total = M + tax_monthly + ins_monthly + hoa + mi_monthly

        if total > allowed_payment:
            high = P
        else:
            low = P

    final_price = low

    # Final payment
    if dp_mode == "percent":
        DP = final_price * (dp_slider / 100)
    else:
        DP = (dp_slider / 100) * dp_max_dollar

    loan_amount = max(final_price - DP, 0)
    M = monthly_mortgage_payment(loan_amount, interest_rate, loan_term)
    tax_monthly = final_price * (property_tax / 100) / 12
    ins_monthly = final_price * (home_insurance / 100) / 12
    mi_monthly = (loan_amount * (mi_pct / 100)) / 12 if mi_pct else 0

    total_monthly = M + tax_monthly + ins_monthly + hoa + mi_monthly

    return {
        "home_value": final_price,
        "monthly_payment": total_monthly,
        "allowed_payment": allowed_payment,
        "exceeds_limit": total_monthly > allowed_payment, 
        "down_payment": DP
    }
