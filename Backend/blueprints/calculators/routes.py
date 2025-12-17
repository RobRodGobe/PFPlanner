from flask import Blueprint, render_template, request
from . import calculators_bp

# Import refactored services
from Backend.services.house_affordability_standard import calculate_affordability
from Backend.services.house_affordability_custom import solve_max_home_price
from Backend.services.sanitize import sanitize_number

# ------------------------------------------------------------
# Calculators Home
# ------------------------------------------------------------
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


@calculators_bp.get("/net-worth-benchmark")
def calc_networth():
    return render_template("coming_soon.html", title="Net Worth Benchmark Calculator")


@calculators_bp.get("/roth-vs-traditional")
def calc_roth():
    return render_template("coming_soon.html", title="Roth vs Traditional Calculator")


@calculators_bp.get("/fine")
def calc_fine():
    return render_template("coming_soon.html", title="FINE Calculator")


# ------------------------------------------------------------
# STANDARD HOUSE AFFORDABILITY CALCULATOR
# ------------------------------------------------------------
@calculators_bp.route("/house-affordability", methods=["GET", "POST"])
def house_affordability():
    errors = {}
    result = None

    # HTMX: toggle MI field
    if request.method == "GET" and request.headers.get("HX-Request") and "toggle_mi" in request.args:
        show = request.args.get("toggle_mi") == "1"
        value = request.args.get("mi_value", "")
        return render_template(
            "calculators/house_affordability/_mortgage_insurance_field.html",
            show=show,
            value=value
        )

    # HTMX: load/collapse advanced fields
    if request.method == "GET" and request.headers.get("HX-Request"):
        show = request.args.get("show") == "1"
        return render_template(
            "calculators/house_affordability/_advanced_fields.html",
            show=show
        )

    # POST: full calculation
    if request.method == "POST":
        income = sanitize_number(request.form.get("income"))
        down_payment = sanitize_number(request.form.get("down_payment"))
        interest_rate = sanitize_number(request.form.get("interest_rate"))
        loan_term = sanitize_number(request.form.get("loan_term"))

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

        if request.headers.get("HX-Request"):
            return render_template(
                "calculators/house_affordability/_results.html",
                errors=errors,
                result=result
            )

    return render_template(
        "calculators/house_affordability/index.html",
        errors=errors,
        result=result
    )


# ------------------------------------------------------------
# CUSTOM HOUSE AFFORDABILITY CALCULATOR
# ------------------------------------------------------------
@calculators_bp.route("/house-affordability/custom", methods=["POST"])
def house_affordability_custom():
    form = request.form

    def s(name):
        return sanitize_number(form.get(name))

    # Income
    income = s("income") or 0
    income_monthly = income / 12

    # Down payment controls
    dp_mode = form.get("dp_mode", "dollar")
    dp_slider = sanitize_number(form.get("down_payment_slider")) or 0
    dp_max_dollar = sanitize_number(form.get("down_payment_max")) or 0

    # Income percentage
    income_pct_slider = sanitize_number(form.get("income_pct_slider")) or 0

    # Loan details
    interest_rate = s("interest_rate") or 0
    loan_term = int(s("loan_term") or 30)

    # Advanced fields
    show_custom_advanced = form.get("custom_advanced_state") == "1"

    property_tax = s("property_tax") if show_custom_advanced else 0
    home_insurance = s("home_insurance") if show_custom_advanced else 0
    hoa = s("hoa") if show_custom_advanced else 0

    include_mi = form.get("include_mi") == "on"
    mi_pct = s("mi_amount") if (show_custom_advanced and include_mi) else 0

    result = solve_max_home_price(
        income_monthly=income_monthly,
        income_pct_limit=income_pct_slider,
        dp_mode=dp_mode,
        dp_slider=dp_slider,
        dp_max_dollar=dp_max_dollar,
        interest_rate=interest_rate,
        loan_term=loan_term,
        property_tax=property_tax or 0,
        home_insurance=home_insurance or 0,
        hoa=hoa or 0,
        mi_pct=mi_pct or 0
    )

    return render_template(
        "calculators/house_affordability/_custom_results.html",
        result=result,
        errors={}
    )


# ------------------------------------------------------------
# TOGGLE BETWEEN STANDARD AND CUSTOM (HTMX)
# ------------------------------------------------------------
@calculators_bp.get("/house-affordability/toggle")
def house_affordability_toggle():
    mode = request.args.get("mode", "standard")

    if mode == "custom":
        return render_template(
            "calculators/house_affordability/_custom_calculator.html",
            errors={},
            result=None
        )

    return render_template(
        "calculators/house_affordability/_standard_calculator.html",
        errors={},
        result=None
    )

# ------------------------------------------------------------
# CUSTOM ADVANCED OPTIONS (HTMX)
# ------------------------------------------------------------
@calculators_bp.get("/house-affordability/custom/advanced")
def house_affordability_custom_advanced():
    show = request.args.get("show") == "1"
    toggle_mi = request.args.get("toggle_mi")

    # Load MI field only
    if toggle_mi is not None:
        show_mi = toggle_mi == "1"
        return render_template(
            "calculators/house_affordability/_mortgage_insurance_field_custom.html",
            show_mi=show_mi
        )

    # Load full advanced fields
    return render_template(
        "calculators/house_affordability/_advanced_fields_custom.html",
        show=show
    )
