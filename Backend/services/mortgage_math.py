import math

def monthly_mortgage_payment(loan_amount, annual_rate, years):
    r = annual_rate / 100 / 12
    n = years * 12

    if r == 0:
        return loan_amount / n

    return loan_amount * (r * (1 + r)**n) / ((1 + r)**n - 1)
