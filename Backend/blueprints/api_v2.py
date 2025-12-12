from flask import Blueprint, jsonify, request, current_app

from Backend.auth.decorators import auth_required

api_v2_bp = Blueprint("api_v2", __name__)


@api_v2_bp.get("/messages")
@auth_required
def list_messages_v2():
    messages = current_app.message_service.get_all()
    data = [
        {
            "id": m.id,
            "text": m.text,
            "created_at": m.created_at.isoformat(),
            "user_id": m.user_id,
        }
        for m in messages
    ]
    return jsonify({"items": data, "count": len(data)}), 200
