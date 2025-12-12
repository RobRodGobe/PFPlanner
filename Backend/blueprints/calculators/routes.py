from flask import render_template
from . import calculators_bp

@calculators_bp.get("/", strict_slashes=False)
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

@calculators_bp.get("/house-affordability")
def calc_house():
    return render_template("coming_soon.html", title="House Affordability Calculator")

@calculators_bp.get("/net-worth-benchmark")
def calc_networth():
    return render_template("coming_soon.html", title="Net Worth Benchmark Calculator")

@calculators_bp.get("/roth-vs-traditional")
def calc_roth():
    return render_template("coming_soon.html", title="Roth vs Traditional Calculator")

@calculators_bp.get("/fine")
def calc_fine():
    return render_template("coming_soon.html", title="FINE Calculator")