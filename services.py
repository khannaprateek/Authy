from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_security import JWTManager
from models.user_model import User
from app import db

jwt_manager = JWTManager()

def create_user_record(user):
    return User.create_user(user)
    

def update_user_information(user, data):
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone_number = data.get('phone_number', user.phone_number)

    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='sha256')

    try:
        db.session.commit()
        return {'message': 'User information updated successfully'}
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error updating user information: {str(e)}'}, 500


def reset_password(user, email):
    if not email:
        return {'message': 'Email is required for password reset'}, 400

    if email != user.email:
        return {'message': 'Invalid email for password reset'}, 400

    new_password = generate_password_hash('new_password', method='sha256')
    user.password = new_password

    try:
        db.session.commit()
        return {'message': 'Password reset successful'}
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error resetting password: {str(e)}'}, 500


def refresh_jwt_token(refresh_token):
    decoded_refresh_token = jwt_manager.decode_refresh_token(refresh_token)

    if decoded_refresh_token:
        user_id = decoded_refresh_token['sub']
        user = User.query.get(user_id)

        if user:
            return jwt_manager.encode_refresh_token(user.id, user.role.name)

    return None