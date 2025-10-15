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
    
    # ✅ Use SQLite for now (simple and local)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telehealth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.models import Patient

    # Tell Flask-Login how to load a patient by ID
    @login_manager.user_loader
    def load_user(user_id):
        return Patient.query.get(int(user_id))  # ⚠️ fixed indentation

    # Redirect unauthorized users to login page
    login_manager.login_view = 'patient.login'  # ✅ replace the None

    from app.routes.auth import auth_bp
    from app.routes.patient import patient_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)

    return app
