import os

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.extensions import db

route = os.getenv('FLASK_ROUTE', '/')
users_bp = Blueprint('users',__name__, url_prefix=route + 'users')

@users_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=generate_password_hash(data.get('password'))
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201


@users_bp.route('/', methods=['GET'])
def get_all():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@users_bp.route('/<int:user_id>', methods=['PATCH'])
def update(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    if 'password' in data:
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated'}), 200
    