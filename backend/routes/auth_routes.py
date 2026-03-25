import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Unauthorized

from backend.extensions import db
from backend.models.user import User


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}

    username = (payload.get("username") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not username or not email or not password:
        raise BadRequest("username, email, and password are required.")
    if len(password) < 6:
        raise BadRequest("Password must be at least 6 characters.")

    user = User(username=username, email=email)

    # Dev-only bootstrap: if BOOTSTRAP_ADMIN_EMAIL matches the registering email,
    # the account is created as admin. Leave unset in production.
    bootstrap_email = (os.getenv("BOOTSTRAP_ADMIN_EMAIL") or "").strip().lower()
    if bootstrap_email and email == bootstrap_email:
        user.is_admin = True

    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists."}), 409

    return jsonify({"message": "Registered successfully.", "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not password or (not email and not username):
        raise BadRequest("Provide username or email and password.")

    query = User.query
    if email:
        user = query.filter(User.email == email).first()
    else:
        user = query.filter(User.username == username).first()

    if not user or not user.check_password(password):
        raise Unauthorized("Invalid credentials.")

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        raise Unauthorized("User not found.")

    return jsonify({"user": user.to_dict()})

