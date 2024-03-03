from app import db
from sqlalchemy import text
from marshmallow import Schema, fields

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
class UserRoleSchema(Schema):
    class Meta:
        model = UserRole

user_role_schema = UserRoleSchema()

# Insert initial data using INSERT ... ON DUPLICATE KEY UPDATE
if UserRole.query.count() == 0:
    # Insert default user roles
    user_role = UserRole(id=1,name='user')
    manager_role = UserRole(id=2,name='manager')
    admin_role = UserRole(id=3,name='admin')

    db.session.add(user_role)
    db.session.add(manager_role)
    db.session.add(admin_role)

    db.session.commit()