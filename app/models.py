# app/models.py

from flask_login import UserMixin
from app import db
from datetime import datetime

# 🧍 Patient Table
class Patient(db.Model, UserMixin):
    __tablename__ = 'patient'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        return f"<Patient {self.name}>"


# 🩺 Doctor Table
class Doctor(db.Model):
    __tablename__ = 'doctor'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    available = db.Column(db.Boolean, default=True)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialty}>"


# 📅 Appointment Table
class Appointment(db.Model):
    __tablename__ = 'appointment'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return f"<Appointment {self.id} - {self.date}>"
