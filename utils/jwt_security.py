import jwt
from datetime import datetime, timedelta

private_key_path = "utils/jwt/private.pem"
public_key_path = "utils/jwt/public.pub"

class JWTManager:
    def __init__(self, algorithm='RS512', token_lifetime_minutes=15, refresh_token_lifetime_days=7):
        with open(private_key_path, 'rb') as private_key_file:
            self.private_key = private_key_file.read()
        with open(public_key_path, 'rb') as public_key_file:
            self.public_key = public_key_file.read()

        self.algorithm = algorithm
        self.token_lifetime = timedelta(minutes=token_lifetime_minutes)
        self.refresh_token_lifetime = timedelta(days=refresh_token_lifetime_days)

    def encode(self, user_id, role):
        now = datetime.utcnow()
        payload = {
            'sub': user_id,
            'role': role,
            'iat': now,
            'exp': now + self.token_lifetime
        }
        token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return token

    def encode_refresh_token(self, user_id, role):
        now = datetime.utcnow()
        payload = {
            'sub': user_id,
            'role': role,
            'iat': now,
            'exp': now + self.refresh_token_lifetime
        }
        refresh_token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return refresh_token

    def decode(self, token):
        try:
            payload = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Invalid token
            return None
    
    def decode_refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.public_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # Refresh token has expired
            return None
        except jwt.InvalidTokenError:
            # Invalid refresh token
            return None

