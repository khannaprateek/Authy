from functools import wraps
from flask import request, g, jsonify
from models.user_role_model import User
from utils.jwt_security import JWTManager

jwt_manager = JWTManager()

def authenticate_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        decoded_token = jwt_manager.decode(token)
        if not decoded_token:
            return jsonify({'message': 'Invalid token'}), 401

        # Check if the user exists in the database
        user = User.query.get(decoded_token['sub'])
        if not user:
            return jsonify({'message': 'User not found'}), 401

        # Set user information in 'g' for access in route methods
        g.user = user

        return func(*args, **kwargs)

    return wrapper
