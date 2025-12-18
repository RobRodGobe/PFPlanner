from Backend.extensions import db
from Backend.models import User


def test_api_jwt_login(client, app):
    with app.app_context():
        u = User(email="jwt@example.com", role="user")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()

    resp = client.post("/api/v1/auth/login", json={
        "email": "jwt@example.com",
        "password": "secret"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
