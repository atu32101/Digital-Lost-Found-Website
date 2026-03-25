from typing import Optional

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from backend.extensions import db
from backend.models.found_items import FoundItem
from backend.models.lost_items import LostItem
from backend.models.user import User


status_bp = Blueprint("status_bp", __name__, url_prefix="/api")


def _current_user():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    return User.query.get(user_id)


def _update_item_status(item, user: User, new_status: str):
    if new_status not in ("claimed", "unclaimed"):
        raise BadRequest("status must be 'claimed' or 'unclaimed'.")

    # Permission: admin can always update, otherwise only the reporter can update.
    if not user.is_admin and item.user_id != user.id:
        raise Forbidden("You do not have permission to update this item.")

    if new_status == "claimed":
        from backend.utils.helpers import utc_now

        item.status = "claimed"
        item.claimed_by_user_id = user.id
        item.claimed_at = utc_now()
    else:
        item.status = "unclaimed"
        item.claimed_by_user_id = None
        item.claimed_at = None

    db.session.commit()
    return item.to_dict(include_contact=True)


@status_bp.post("/lost-items/<int:item_id>/status")
@jwt_required()
def set_lost_item_status(item_id: int):
    user = _current_user()
    if not user:
        return jsonify({"error": "Unauthorized."}), 401

    payload = request.get_json(silent=True) or {}
    new_status: Optional[str] = payload.get("status")
    if not new_status:
        raise BadRequest("Missing 'status'.")

    item = LostItem.query.get(item_id)
    if not item:
        raise NotFound("Lost item not found.")

    data = _update_item_status(item, user, new_status)
    return jsonify({"message": "Status updated.", "item": data})


@status_bp.post("/found-items/<int:item_id>/status")
@jwt_required()
def set_found_item_status(item_id: int):
    user = _current_user()
    if not user:
        return jsonify({"error": "Unauthorized."}), 401

    payload = request.get_json(silent=True) or {}
    new_status: Optional[str] = payload.get("status")
    if not new_status:
        raise BadRequest("Missing 'status'.")

    item = FoundItem.query.get(item_id)
    if not item:
        raise NotFound("Found item not found.")

    data = _update_item_status(item, user, new_status)
    return jsonify({"message": "Status updated.", "item": data})

