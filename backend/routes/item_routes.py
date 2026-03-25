from typing import Optional

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest, NotFound

from backend.extensions import db
from backend.models.found_items import FoundItem
from backend.models.lost_items import LostItem
from backend.models.user import User
from backend.utils.helpers import parse_date, save_upload_image


item_bp = Blueprint("item_bp", __name__, url_prefix="/api")


def _get_current_user():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    return User.query.get(user_id)


def _apply_filters(query, model, keyword: Optional[str], category: Optional[str], status: Optional[str]):
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(or_(model.title.ilike(kw), model.description.ilike(kw)))
    if category:
        query = query.filter(model.category == category)
    if status:
        query = query.filter(model.status == status)
    return query


@item_bp.post("/lost-items")
@jwt_required()
def create_lost_item():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized."}), 401

    form = request.form
    title = (form.get("title") or "").strip()
    description = (form.get("description") or "").strip()
    category = (form.get("category") or "").strip() or None
    location = (form.get("location") or "").strip() or None
    contact_email = (form.get("contact_email") or "").strip() or None
    contact_phone = (form.get("contact_phone") or "").strip() or None

    date = parse_date(form.get("date"))
    if not title or not date:
        raise BadRequest("title and date are required.")

    storage = request.files.get("image")
    image_filename = None
    if storage and storage.filename:
        image_filename = save_upload_image(storage, current_app.config["UPLOAD_FOLDER"])

    item = LostItem(
        user_id=user.id,
        title=title,
        description=description,
        category=category,
        date=date,
        location=location,
        image_filename=image_filename,
        contact_email=contact_email,
        contact_phone=contact_phone,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Lost item created.", "item": item.to_dict(include_contact=True)}), 201


@item_bp.post("/found-items")
@jwt_required()
def create_found_item():
    user = _get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized."}), 401

    form = request.form
    title = (form.get("title") or "").strip()
    description = (form.get("description") or "").strip()
    category = (form.get("category") or "").strip() or None
    location = (form.get("location") or "").strip() or None
    contact_email = (form.get("contact_email") or "").strip() or None
    contact_phone = (form.get("contact_phone") or "").strip() or None

    date = parse_date(form.get("date"))
    if not title or not date:
        raise BadRequest("title and date are required.")

    storage = request.files.get("image")
    image_filename = None
    if storage and storage.filename:
        image_filename = save_upload_image(storage, current_app.config["UPLOAD_FOLDER"])

    item = FoundItem(
        user_id=user.id,
        title=title,
        description=description,
        category=category,
        date=date,
        location=location,
        image_filename=image_filename,
        contact_email=contact_email,
        contact_phone=contact_phone,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Found item created.", "item": item.to_dict(include_contact=True)}), 201


@item_bp.get("/lost-items")
def list_lost_items():
    keyword = (request.args.get("keyword") or "").strip() or None
    category = (request.args.get("category") or "").strip() or None
    status = (request.args.get("status") or "").strip() or None

    query = LostItem.query.order_by(LostItem.created_at.desc())
    query = _apply_filters(query, LostItem, keyword, category, status)
    items = query.all()
    return jsonify({"items": [i.to_dict(include_contact=True) for i in items]})


@item_bp.get("/found-items")
def list_found_items():
    keyword = (request.args.get("keyword") or "").strip() or None
    category = (request.args.get("category") or "").strip() or None
    status = (request.args.get("status") or "").strip() or None

    query = FoundItem.query.order_by(FoundItem.created_at.desc())
    query = _apply_filters(query, FoundItem, keyword, category, status)
    items = query.all()
    return jsonify({"items": [i.to_dict(include_contact=True) for i in items]})


@item_bp.get("/lost-items/<int:item_id>")
def lost_item_details(item_id: int):
    item = LostItem.query.get(item_id)
    if not item:
        raise NotFound("Lost item not found.")
    return jsonify({"item": item.to_dict(include_contact=True)})


@item_bp.get("/found-items/<int:item_id>")
def found_item_details(item_id: int):
    item = FoundItem.query.get(item_id)
    if not item:
        raise NotFound("Found item not found.")
    return jsonify({"item": item.to_dict(include_contact=True)})

