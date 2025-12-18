from Backend.app import create_app

def test_custom_results_renders():
    app = create_app("testing")
    with app.app_context():
        env = app.jinja_env
        template = env.get_template("calculators/house_affordability/_custom_results.html")

        html = template.render(result={
            "home_value": 500000,
            "monthly_payment": 2500,
            "allowed_payment": 3000,
            "exceeds_limit": False,
            "down_payment": 100000
        })

        assert "Total Financed Amount" in html
        assert "$400,000" in html
