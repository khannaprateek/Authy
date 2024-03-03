from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
ma = Marshmallow(app)



if __name__ == '__main__':
    with app.app_context():
        # Create tables if not exist
        db.init_app(app)
        db.create_all()

    app.run(debug=True)
