from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Doctor, Appointment

doctor_bp = Blueprint('doctor', __name__)

# ---------------------------
# Doctor Login
# ---------------------------
@doctor_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and hasattr(current_user, 'specialty'):
        return redirect(url_for('doctor.dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and bcrypt.check_password_hash(doctor.password, password):
            login_user(doctor)
            flash(f'Welcome Dr. {doctor.name}!', 'success')
            return redirect(url_for('doctor.dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('doctor_login.html')


# ---------------------------
# Doctor Dashboard
# ---------------------------
@doctor_bp.route('/dashboard')
@login_required
def dashboard():
    if not hasattr(current_user, 'specialty'):
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.login'))

    # Get all appointments for this doctor
    appointments = Appointment.query.filter_by(doctor_id=current_user.id).order_by(Appointment.date).all()
    return render_template('doctor_dashboard.html', appointments=appointments, current_user=current_user)


# ---------------------------
# Doctor Logout
# ---------------------------
@doctor_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('doctor.login'))
