import logging
import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_limiter import Limiter
from argon2 import PasswordHasher
from db.models import Users, Languages, Roles
from extentions import db


logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)
limiter = Limiter(__name__)


@auth_bp.route("/auth/register")
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    username = data.get("username")
    if not is_username_free(username):
        return jsonify("Username is already registered"), 400
    password_check = is_password_not_valid(data.get("password"))
    if password_check:
        return jsonify(password_check), 400
    password = create_password_hash(data.get("password"))
    language = data.get("language")
    user = Users(username=username,
                 password=password,
                 language=get_language_id(language),
                 role=get_role_id("user"))
    db.session.add(user)
    db.session.commit()


@auth_bp.route("/auth/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")


def create_password_hash(password):
    pwh = PasswordHasher()
    return pwh.hash(password)


def is_password_hash_valid(password, password_hash_in_database):
    pwh = PasswordHasher()
    return pwh.verify(password_hash_in_database, password)


def is_password_not_valid(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r'[a-zA-Z]', password):
        return "Password must contain at least one Latin letter"
    if not re.search(r'[!@#$%^&()*_+=-]', password):
        return "Password must contain at least one special character (!@#$%^&()*_+=-)"
    if re.search(r'[^a-zA-Z!@#$%^&()*_+=-]', password):
        return "Password can only contain Latin letters and special characters (!@#$%^&()*_+=-)"
    return None


def is_username_free(username):
    return True if Users.query.filter_by(username=username).first() else False


def get_role_id(role):
    role = Roles.query.filter_by(role=role).first()
    if role:
        return role.id


def get_language_id(language):
    lang = Languages.query.filter_by(language=language).first()
    if lang:
        return lang.id
