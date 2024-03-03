from app import app
from flask import request, jsonify, g

from services import create_user, refresh_jwt_token, reset_password, update_user_information
from utils.decorator import authenticate_user
from utils.otp_service import create_otp, verify_otp

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    result, status_code = create_user(data)
    return jsonify(result), status_code

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    result, status_code = create_otp(data.code, data.phone_number)
    return jsonify(result), status_code

@app.route('/verify-otp', methods=['POST'])
def login_user():
    data = request.json
    result, status_code = verify_otp(data.id, data.code)
    return jsonify(result), status_code

@app.route('/update_user', methods=['PUT'])
@authenticate_user
def update_user():
    data = request.json
    user = g.user
    result, status_code = update_user_information(user, data)
    return jsonify(result), status_code


@app.route('/reset_password', methods=['POST'])
@authenticate_user
def reset_password_route():
    data = request.json
    user = g.user
    result, status_code = reset_password(user, data.get('email'))
    return jsonify(result), status_code
    

@app.route('/refresh_token', methods=['POST'])
def refresh_token():
    data = request.json
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 400

    new_tokens = refresh_jwt_token(refresh_token)

    if new_tokens:
        return jsonify({'token': new_tokens['jwt_token'], 'refresh_token': new_tokens['refresh_token']})

    return jsonify({'message': 'Invalid refresh token'}), 401
