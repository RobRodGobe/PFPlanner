from flask import Blueprint, jsonify, request, current_app
from Backend.auth.decorators import auth_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Backend.models import User
from Backend.extensions import db
from Backend.auth.decorators import auth_required

api_v1_bp = Blueprint("api_v1", __name__)

@api_v1_bp.post("/auth/login")
def api_login():
    payload = request.get_json() or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_access_token(identity=user)
    return jsonify({"access_token": token}), 200

from Backend.auth.roles import role_required

@api_v1_bp.delete("/messages/<int:message_id>")
@role_required("admin")
def delete_message(message_id):
    # TODO: delete logic
    ...


# Example: list messages
@api_v1_bp.get("/messages")
@auth_required
def list_messages():
    messages = current_app.message_service.get_all()
    data = [
        {"id": m.id, "text": m.text, "created_at": m.created_at.isoformat()}
        for m in messages
    ]
    return jsonify(data), 200


# Example: create a message
@api_v1_bp.post("/messages")
@auth_required
def create_message():
    payload = request.get_json() or {}
    text = payload.get("text")
    if not text:
        return jsonify({"error": "text is required"}), 400

    msg = current_app.message_service.add(text)
    return jsonify({
        "id": msg.id,
        "text": msg.text,
        "created_at": msg.created_at.isoformat()
    }), 201
