from functools import wraps

from flask import jsonify, session


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "authentication required"}), 401
        return view(*args, **kwargs)

    return wrapped
