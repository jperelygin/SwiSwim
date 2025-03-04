import logging
import re
from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from argon2 import PasswordHasher
from app.db.models import Users, Languages, Roles
from app import app


logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)
limiter = Limiter(__name__)


@auth_bp.route("/register", methods=["POST"])
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
    email = data.get("email")
    if not is_email_unique(email):
        return jsonify("Email is already registered"), 400
    if not is_email_valid(email):
        return jsonify("Email is not in valid format"), 400
    language = data.get("language")
    user = Users(username=username,
                 password_hash=password,
                 email=email,
                 language=get_language_id(language),
                 role=get_role_id("user")
                 )
    app.db.session.add(user)
    app.db.session.commit()
    return jsonify({"message": f"User {username!r} created!"}), 201


@auth_bp.route("/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")


def is_password_hash_valid(password, password_hash_in_database):
    pwh = PasswordHasher()
    return pwh.verify(password_hash_in_database, password)


def is_password_not_valid(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r'[a-zA-Z]', password):
        return "Password must contain at least one Latin letter"
    if not re.search(r'[0-9]', password):  # Check for at least one digit
        return "Password must contain at least one number"
    if not re.search(r'[!@#$%^&()*_+=-]', password):
        return "Password must contain at least one special character (!@#$%^&()*_+=-)"
    if re.search(r'[^a-zA-Z0-9!@#$%^&()*_+=-]', password):  # Allow letters, digits, and special characters
        return "Password can only contain Latin letters, numbers, and special characters (!@#$%^&()*_+=-)"
    return None

def create_password_hash(password):
    pwh = PasswordHasher()
    return pwh.hash(password)


def is_email_unique(email):
    return True if not Users.query.filter_by(email=email).first() else False


def is_email_valid(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


def is_username_free(username):
    return True if not Users.query.filter_by(username=username).first() else False


def get_role_id(role):
    return Roles.query.filter_by(role=role).first()


def get_language_id(language):
    return Languages.query.filter_by(language=language).first()
