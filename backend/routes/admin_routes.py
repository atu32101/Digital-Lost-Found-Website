from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import Forbidden, NotFound

from backend.extensions import db
from backend.models.found_items import FoundItem
from backend.models.lost_items import LostItem
from backend.models.user import User


admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")


def _current_admin():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        raise Forbidden("Admin access required.")
    return user


@admin_bp.get("/lost-items")
@jwt_required()
def admin_list_lost_items():
    _current_admin()
    items = LostItem.query.order_by(LostItem.created_at.desc()).all()
    return jsonify({"items": [i.to_dict(include_contact=True) for i in items]})


@admin_bp.get("/found-items")
@jwt_required()
def admin_list_found_items():
    _current_admin()
    items = FoundItem.query.order_by(FoundItem.created_at.desc()).all()
    return jsonify({"items": [i.to_dict(include_contact=True) for i in items]})


@admin_bp.delete("/lost-items/<int:item_id>")
@jwt_required()
def admin_delete_lost_item(item_id: int):
    _current_admin()
    item = LostItem.query.get(item_id)
    if not item:
        raise NotFound("Lost item not found.")
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Lost item deleted."})


@admin_bp.delete("/found-items/<int:item_id>")
@jwt_required()
def admin_delete_found_item(item_id: int):
    _current_admin()
    item = FoundItem.query.get(item_id)
    if not item:
        raise NotFound("Found item not found.")
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Found item deleted."})

