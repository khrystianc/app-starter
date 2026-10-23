"""Routes: which URL does what."""
from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return "It works. Replace this page with the real app."


@bp.get("/health")
def health():
    # Render pings this after each deploy. Keep it fast and dependency-free.
    return jsonify(status="ok")
