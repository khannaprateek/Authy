from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from app import db, ma
from models.user_role_model import UserRole

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    role = db.relationship('UserRole', backref='users')

    @staticmethod
    def create_user(data):
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=hashed_password,
            role_id = UserRole.query().filter_by(name="user").first().id
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user)
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Email or phone number already exists'}, 400

    @staticmethod
    def login_user(data):
        user = User.query.filter_by(phone_number=data['phone_number']).first()

        if user and check_password_hash(user.password, data['password']):
            return {'message': 'Login successful', 'token': User.generate_jwt_token(user)}
        else:
            return {'message': 'Invalid credentials'}, 401

    @staticmethod
    def generate_jwt_token(user):
        # Implementation required for generating JWT token
        pass
    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)