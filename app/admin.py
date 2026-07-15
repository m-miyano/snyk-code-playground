import subprocess

from flask import Blueprint, jsonify, request

from app.decorators import login_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/ping")
@login_required
def ping():
    # Lets support quickly check connectivity to a host from the server.
    host = request.args.get("host", "127.0.0.1")
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return jsonify({"host": host, "output": output.decode(errors="replace")})
