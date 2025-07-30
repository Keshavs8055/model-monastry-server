from flask import Blueprint
from api.controllers.user_controller import register_user, login_user

auth_bp = Blueprint("auth_bp", __name__)

auth_bp.route("/register", methods=["POST"])(register_user)
auth_bp.route("/login", methods=["POST"])(login_user)
