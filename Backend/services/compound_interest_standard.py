def compound_growth(
    initial,
    monthly_contribution,
    annual_rate,
    years,
    contribution_timing="end",   # "beginning" or "end"
    frequency="monthly",         # "monthly" or "annual"
    annual_contribution=0,
    compounding="annual"         # "monthly" or "annual"
):
    """
    Universal compound interest engine following Roberto's rules:

    1. Start with current balance.
    2. If timing = beginning → add contribution BEFORE compounding.
    3. Apply compounding:
         - monthly → interest every month at r/12
         - annual → interest once per year at r
    4. If timing = end → add contribution AFTER compounding.
    5. Contribution frequency is independent of compounding frequency.
    """

    years = int(years)
    months = years * 12
    r = annual_rate / 100.0
    monthly_rate = r / 12.0

    balance = initial
    total_contributions = initial
    breakdown = []

    principal = 1000
    rate = 0.05  # 5% annual interest rate
    time = 3     # 3 years

    amount = principal
    for year in range(1, time + 1):
        amount = amount * (1 + rate)
        print(f"Year {year}: ${amount:.2f}")

    for m in range(1, months + 1):
        is_start_of_year = (m % 12 == 1)
        is_end_of_year = (m % 12 == 0)

        # ============================================================
        # 1. BEGINNING-OF-PERIOD CONTRIBUTIONS
        # ============================================================
        if contribution_timing == "beginning":
            if frequency == "monthly":
                balance += monthly_contribution
                total_contributions += monthly_contribution
            else:  # annual contributions
                if is_start_of_year:
                    balance += annual_contribution
                    total_contributions += annual_contribution

        # ============================================================
        # 2. GROWTH (COMPOUNDING)
        # ============================================================
        if compounding == "monthly":
            # Apply monthly interest every month
            balance *= (1 + monthly_rate)
        else:
            # Apply annual interest once per year
            if is_end_of_year:
                balance *= (1 + r)

        # ============================================================
        # 3. END-OF-PERIOD CONTRIBUTIONS
        # ============================================================
        if contribution_timing == "end":
            if frequency == "monthly":
                balance += monthly_contribution
                total_contributions += monthly_contribution
            else:  # annual contributions
                if is_end_of_year:
                    balance += annual_contribution
                    total_contributions += annual_contribution

        # ============================================================
        # 4. END-OF-YEAR SNAPSHOT
        # ============================================================
        if is_end_of_year:
            breakdown.append({
                "year": m // 12,
                "balance": balance,
                "contributions": total_contributions,
                "growth": balance - total_contributions
            })

    return {
        "ending_balance": balance,
        "total_contributions": total_contributions,
        "total_growth": balance - total_contributions,
        "yearly_breakdown": breakdown,
    }
