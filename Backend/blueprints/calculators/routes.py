from flask import Blueprint, render_template, request
from markupsafe import escape
from . import calculators_bp

def sanitize_number(value):
    """Remove commas, spaces, and convert to float safely."""
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None

@calculators_bp.get("/")
def calculators_home():
    return render_template("calculators/index.html")

@calculators_bp.get("/compound-interest")
def calc_compound():
    return render_template("coming_soon.html", title="Compound Interest Calculator")

@calculators_bp.get("/wealth-multiplier")
def calc_wealth():
    return render_template("coming_soon.html", title="Wealth Multiplier Calculator")

@calculators_bp.get("/car-affordability")
def calc_car():
    return render_template("coming_soon.html", title="Car Affordability Calculator")

@calculators_bp.route("/house-affordability", methods=["GET", "POST"])
def house_affordability():
    errors = {}
    result = None
    
    # HTMX: toggle MI field
    if request.method == "GET" and request.headers.get("HX-Request") and "toggle_mi" in request.args:
        show = request.args.get("toggle_mi") == "1"
        value = request.args.get("mi_value", "")
        return render_template("calculators/_mortgage_insurance_field.html", show=show, value=value)

    # HTMX: load/collapse advanced fields only
    if request.method == "GET" and request.headers.get("HX-Request"):
        show = request.args.get("show") == "1"
        return render_template(
            "calculators/_advanced_fields.html",
            show=show
        )

    if request.method == "POST":
        # Required fields
        income = sanitize_number(request.form.get("income"))
        down_payment = sanitize_number(request.form.get("down_payment"))
        interest_rate = sanitize_number(request.form.get("interest_rate"))
        loan_term = sanitize_number(request.form.get("loan_term"))

        # Optional fields
        property_tax = sanitize_number(request.form.get("property_tax"))
        home_insurance = sanitize_number(request.form.get("home_insurance"))
        hoa = sanitize_number(request.form.get("hoa"))
        include_mi = request.form.get("include_mi") == "on"
        mi_amount = sanitize_number(request.form.get("mi_amount"))

        # Validation
        if income is None or income <= 0:
            errors["income"] = "Annual income is required and must be a positive number."

        if down_payment is None or down_payment < 0:
            errors["down_payment"] = "Down payment is required and must be a valid number."

        if interest_rate is None or interest_rate <= 0:
            errors["interest_rate"] = "Interest rate is required and must be a positive number."

        if loan_term is None or loan_term <= 0:
            errors["loan_term"] = "Loan term is required and must be a positive number."            

        if include_mi and (mi_amount is None or mi_amount < 0):
            errors["mi_amount"] = "Mortgage insurance amount is required when MI is enabled."

        # Only calculate if valid
        if not errors:
            result = calculate_affordability(
                income=income,
                down_payment=down_payment,
                interest_rate=interest_rate,
                loan_term=loan_term,
                property_tax=property_tax,
                home_insurance=home_insurance,
                hoa=hoa,
                include_mi=include_mi,
                mi_amount=mi_amount,
            )

        # HTMX POST: return only results partial
        if request.headers.get("HX-Request"):
            return render_template(
                "calculators/_house_affordability_results.html",
                errors=errors,
                result=result
            )

    # ✅ FULL PAGE GET (this was missing!)
    return render_template(
        "calculators/house_affordability.html",
        errors=errors,
        result=result
    )
        
def calculate_affordability(
    income,
    down_payment,
    interest_rate,
    loan_term,
    property_tax=None,      # percent (e.g., 0.2 for 0.2%)
    home_insurance=None,    # percent
    hoa=None,               # dollars per month
    include_mi=False,
    mi_amount=None,         # percent (e.g., 1 for 1%)
):
    monthly_income = income / 12
    max_housing_ratio = 0.25
    max_monthly_payment = monthly_income * max_housing_ratio

    r = (interest_rate / 100) / 12
    n = loan_term * 12

    # Convert percentages to decimals
    tax_rate = (property_tax / 100) if property_tax else 0
    ins_rate = (home_insurance / 100) if home_insurance else 0
    mi_rate  = (mi_amount / 100) if (include_mi and mi_amount) else 0

    # Initial guess
    home_value = 200000.0

    for _ in range(8):  # MG uses ~5–8 iterations
        mortgage_amount = home_value - down_payment

        # MI only if LTV > 80%
        if include_mi and mortgage_amount / home_value > 0.80:
            annual_mi = mortgage_amount * mi_rate
            monthly_mi = annual_mi / 12
        else:
            monthly_mi = 0

        # Costs based on home value
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

        # Money Guy rounds amortization factor to 8 decimals
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


@calculators_bp.get("/net-worth-benchmark")
def calc_networth():
    return render_template("coming_soon.html", title="Net Worth Benchmark Calculator")

@calculators_bp.get("/roth-vs-traditional")
def calc_roth():
    return render_template("coming_soon.html", title="Roth vs Traditional Calculator")

@calculators_bp.get("/fine")
def calc_fine():
    return render_template("coming_soon.html", title="FINE Calculator")