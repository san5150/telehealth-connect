from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-to-a-strong-secret'
    # Placeholder DB URI; you'll replace with a cloud DB or local DB credentials
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user:pass@host/dbname'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.patient import patient_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)

    return app
