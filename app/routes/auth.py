from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, bcrypt
from app.models import Patient
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

# ---------------------------
# REGISTER ROUTE
# ---------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('patient.dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_patient = Patient.query.filter_by(email=email).first()
        if existing_patient:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.login'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_patient = Patient(name=name, email=email, password=hashed_pw)
        db.session.add(new_patient)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# ---------------------------
# LOGIN ROUTE
# ---------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('patient.dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        patient = Patient.query.filter_by(email=email).first()
        if patient and bcrypt.check_password_hash(patient.password, password):
            login_user(patient)
            flash(f'Welcome, {patient.name}!', 'success')
            return redirect(url_for('patient.dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')


# ---------------------------
# LOGOUT ROUTE
# ---------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
