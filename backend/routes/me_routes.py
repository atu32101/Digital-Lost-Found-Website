from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.models.found_items import FoundItem
from backend.models.lost_items import LostItem
from backend.models.user import User


me_bp = Blueprint("me_bp", __name__, url_prefix="/api/me")


@me_bp.get("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "Unauthorized."}), 401

    lost_items = (
        LostItem.query.filter(LostItem.user_id == user.id)
        .order_by(LostItem.created_at.desc())
        .all()
    )
    found_items = (
        FoundItem.query.filter(FoundItem.user_id == user.id)
        .order_by(FoundItem.created_at.desc())
        .all()
    )

    return jsonify(
        {
            "lost_items": [i.to_dict(include_contact=True) for i in lost_items],
            "found_items": [i.to_dict(include_contact=True) for i in found_items],
            "me": user.to_dict(),
        }
    )

