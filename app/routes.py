from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, HealthData
import pandas as pd
import pdfkit
import os

main_bp = Blueprint('main', __name__)

# Route to show the database path (index)
@main_bp.route('/')
def index():
    db_path = db.engine.url
    return f"Database path: {db_path}"

# Route for the dashboard
@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    health_data = HealthData.query.all()  # Fetch all health data for the dashboard
    states = HealthData.query.with_entities(HealthData.state).distinct()  # Get distinct states
    filtered_data = []

    if request.method == 'POST':
        state = request.form.get('state')
        district = request.form.get('district')

        # Filter health data based on state and district
        filtered_data = HealthData.query
        if state:
            filtered_data = filtered_data.filter(HealthData.state == state)
        if district:
            filtered_data = filtered_data.filter(HealthData.district == district)
        filtered_data = filtered_data.all()

    return render_template('dashboard.html', data=filtered_data if filtered_data else health_data, user=current_user, states=states)

# Route for filtering health data
@main_bp.route('/filter-health-data', methods=['POST'])
@login_required
def filter_health_data():
    # Extract filter inputs from the request form
    filters = {key: request.form.get(key) for key in request.form.keys()}

    # Start building the query
    query = HealthData.query  # Adjust to your actual model name

    # Apply filters only if the value is provided
    for key, value in filters.items():
        if value:
            if key in ['tb_incidence', 'diabetes', 'malaria_incidence', 'hiv_aids', 'imr', 'vaccination', 'income', 'employment_rate', 'education', 'housing', 'urbanization', 'aqi', 'annual_rainfall']:
                query = query.filter(getattr(HealthData, key) >= float(value))
            elif key == 'healthcare_access':
                query = query.filter(HealthData.target_healthcare_access == int(value))
            else:
                query = query.filter(getattr(HealthData, key) == value)

    # Execute the filtered query
    filtered_data = query.all()

    # Render the dashboard with the filtered data
    states = HealthData.query.with_entities(HealthData.state).distinct()  # Get distinct states for the dropdown
    return render_template('dashboard.html', data=filtered_data, user=current_user, states=states)

# Route to fetch health data (for API use)
@main_bp.route('/health-data', methods=['GET'])
def get_health_data():
    try:
        data = HealthData.query.all()  # Fetch all records
        return jsonify([record.to_dict() for record in data])  # Assuming you have a to_dict method
    except Exception as e:
        print(f"Error fetching health data: {e}")
        return jsonify({"error": str(e)}), 500

# Authentication routes
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Login failed. Check your email and password.')
    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! You can now log in.')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main_bp.route('/get-districts', methods=['GET'])
@login_required
def get_districts():
    state = request.args.get('state')
    districts = HealthData.query.with_entities(HealthData.district).filter(HealthData.state == state).distinct().all()
    return jsonify([district[0] for district in districts])

@main_bp.route('/get-metrics', methods=['GET'])
@login_required
def get_metrics():
    state = request.args.get('state')
    district = request.args.get('district')
    # Query the database to get the relevant health metrics based on state/district
    metrics = HealthData.query.filter(
        HealthData.state == state,
        HealthData.district == district
    ).first()  # Adjust to fetch the desired metrics
    return jsonify(metrics.to_dict() if metrics else {})

# Route to download health data as CSV
@main_bp.route('/download_csv', methods=['GET'])
@login_required
def download_csv():
    data = HealthData.query.all()
    df = pd.DataFrame([record.to_dict() for record in data])  # Ensure you have a to_dict method on your model
    csv_file = 'health_data.csv'
    df.to_csv(csv_file, index=False)
    return send_file(csv_file, as_attachment=True)

# Route to download health data as PDF
@main_bp.route('/download_pdf', methods=['GET'])
@login_required
def download_pdf():
    data = HealthData.query.all()
    # Convert data to HTML table for PDF
    html = render_template('pdf_template.html', data=data)
    pdf_file = 'health_report.pdf'
    pdfkit.from_string(html, pdf_file)
    return send_file(pdf_file, as_attachment=True)

# Ensure temporary files are cleaned up after downloading
@main_bp.after_request
def cleanup(response):
    try:
        os.remove('health_data.csv')
        os.remove('health_report.pdf')
    except Exception as e:
        print(f"Cleanup error: {e}")
    return response
