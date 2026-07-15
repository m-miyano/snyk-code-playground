from flask import Blueprint, abort, jsonify, request, session

from app import db
from app.decorators import login_required
from app.models import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def _serialize(task):
    return {"id": task.id, "title": task.title, "done": task.done}


def _get_owned_task_or_404(task_id):
    task = Task.query.filter_by(
        id=task_id, user_id=session["user_id"]
    ).first()
    if task is None:
        abort(404)
    return task


@tasks_bp.get("")
@login_required
def list_tasks():
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([_serialize(t) for t in tasks])


@tasks_bp.post("")
@login_required
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    task = Task(title=title, user_id=session["user_id"])
    db.session.add(task)
    db.session.commit()
    return jsonify(_serialize(task)), 201


@tasks_bp.patch("/<int:task_id>")
@login_required
def update_task(task_id):
    task = _get_owned_task_or_404(task_id)
    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        task.title = title
    if "done" in data:
        task.done = bool(data.get("done"))

    db.session.commit()
    return jsonify(_serialize(task))


@tasks_bp.delete("/<int:task_id>")
@login_required
def delete_task(task_id):
    task = _get_owned_task_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204
