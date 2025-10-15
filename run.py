# run.py
from app import create_app, db
from app.models import Patient, Doctor, Appointment

app = create_app()

if __name__ == '__main__':
    # Create database tables if they don't exist (only do this in dev)
    with app.app_context():
        db.create_all()
    
    # Bind to 0.0.0.0 so Codespaces can expose the port
    app.run(host='0.0.0.0', port=5000, debug=True)
