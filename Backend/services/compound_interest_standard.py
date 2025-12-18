def compound_growth(
    initial,
    monthly,
    annual_rate,
    years,
    contribution_timing="end",  # "beginning" or "end"
):
    """
    Returns:
        {
            "ending_balance": float,
            "total_contributions": float,
            "total_growth": float,
            "yearly_breakdown": [
                {"year": 1, "balance": ..., "contributions": ..., "growth": ...},
                ...
            ]
        }
    """

    r = annual_rate / 100
    monthly_rate = r / 12
    years = int(years)
    months = years * 12

    balance = initial
    total_contributions = initial
    breakdown = []

    for m in range(1, months + 1):
        if contribution_timing == "beginning":
            balance += monthly
            total_contributions += monthly

        balance *= (1 + monthly_rate)

        if contribution_timing == "end":
            balance += monthly
            total_contributions += monthly

        # End of each year → record snapshot
        if m % 12 == 0:
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
