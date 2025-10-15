from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Doctor, Appointment
from app import db
from datetime import datetime

patient_bp = Blueprint('patient', __name__)

# 🏠 Home route
@patient_bp.route('/')
def home():
    return render_template('home.html')

# 🏥 Patient Dashboard
@patient_bp.route('/dashboard')
@login_required
def dashboard():
    doctors = Doctor.query.all()
    return render_template('dashboard.html', doctors=doctors, current_user=current_user)


# 📅 Book Appointment route (POST method)
@patient_bp.route('/book/<int:doctor_id>', methods=['POST'])
@login_required
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Get appointment date from form
    appointment_date_str = request.form.get('appointment_date')
    if not appointment_date_str:
        flash('Please select a valid date and time.', 'danger')
        return redirect(url_for('patient.dashboard'))

    try:
        appointment_date = datetime.fromisoformat(appointment_date_str)
    except ValueError:
        flash('Invalid date format.', 'danger')
        return redirect(url_for('patient.dashboard'))

    appointment = Appointment(
        patient_id=current_user.id,
        doctor_id=doctor.id,
        date=appointment_date
    )
    db.session.add(appointment)
    db.session.commit()

    flash(f'Appointment booked with {doctor.name} on {appointment_date.strftime("%Y-%m-%d %H:%M")}!', 'success')
    return redirect(url_for('patient.dashboard'))

# 📄 View My Appointments
@patient_bp.route('/my_appointments')
@login_required
def my_appointments():
    # Get all appointments for the current patient
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.date.asc()).all()
    return render_template('my_appointments.html', appointments=appointments)
# ❌ Cancel Appointment
@patient_bp.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Only allow the patient who booked it to cancel
    if appointment.patient_id != current_user.id:
        flash("You are not authorized to cancel this appointment.", "danger")
        return redirect(url_for('patient.my_appointments'))

    db.session.delete(appointment)
    db.session.commit()
    flash(f"Appointment with Dr. {appointment.doctor.name} on {appointment.date.strftime('%Y-%m-%d %H:%M')} canceled.", "success")
    return redirect(url_for('patient.my_appointments'))
