from flask import Blueprint, request, jsonify, current_app, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def home():
    return render_template("main_page.html")
