from flask import Flask, request, jsonify, render_template, make_response
from flask_login import login_required
from sqlalchemy import create_engine
import pandas as pd
from fpdf import FPDF  # For PDF generation
from app.models import HealthData, Resource  # Import your models

app = Flask(__name__)

# Create a database engine (SQLite in this case, but can be any database)
engine = create_engine('sqlite:///C:/Users/abiji/Desktop/project-root/database.db')

# Define ranges for health metrics
RANGES = {
    'TB Incidence': [328.13, 654.57],
    'Diabetes': [9.29, 17.09],
    'Malaria Incidence': [166.40, 332.70],
    'HIV/AIDS': [16.73, 33.37],
    'IMR': [82.01, 164.00],
    'Vaccination': [53.33, 76.67],
    'Income': [66245, 132489],
    'Employment Rate': [16394, 32786],
    'Education': [33.58, 66.65],
    'Housing': [32.93, 63.86],
    'Urbanization': [34.67, 67.33],
    'AQI': [106.00, 202.00],
    'Annual Rainfall': [1620.04, 3175.07],
    'Healthcare Access': [0, 4]
}

# Function to categorize data based on ranges
def categorize_value(metric, value):
    low, medium = RANGES.get(metric, [0, 0])
    if value <= low:
        return 'low'
    if value <= medium:
        return 'medium'
    return 'high'

# Route to load CSV data into the database
@app.route('/load-csv', methods=['GET'])
def load_csv_to_db():
    df = pd.read_csv('data/health_data.csv')
    df.to_sql('health_data', engine, if_exists='replace', index=False)
    return jsonify({"message": "Data loaded and written to the database successfully!"})

# Route to retrieve all data from the database
@app.route('/get-data', methods=['GET'])
def get_data():
    with engine.connect() as connection:
        result = pd.read_sql("SELECT * FROM health_data", connection)  
    data = result.to_dict(orient='records')
    return jsonify(data)

# Route for rendering the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route to filter data for charts 
@app.route('/filter-health-data', methods=['POST'])
def filter_health_data():
    state = request.form.get('state')
    district = request.form.get('district')
    metric = request.form.get('metric')

    # Query the database and filter based on state and optionally district
    with engine.connect() as connection:
        query = f"SELECT * FROM health_data WHERE State = '{state}'"
        if district:
            query += f" AND District = '{district}'"
        filtered_data = pd.read_sql(query, connection)

    # Categorize metric data
    filtered_data['Category'] = filtered_data[metric].apply(lambda x: categorize_value(metric, x))

    # Count occurrences of low, medium, and high categories
    low_count = filtered_data[filtered_data['Category'] == 'low'].shape[0]
    medium_count = filtered_data[filtered_data['Category'] == 'medium'].shape[0]
    high_count = filtered_data[filtered_data['Category'] == 'high'].shape[0]

    # Return the result for chart rendering
    return jsonify({
        'low': low_count,
        'medium': medium_count,
        'high': high_count
    })

# Route to filter data for map visualization (Healthcare Access)
@app.route('/filter-map-data', methods=['POST'])
def filter_map_data():
    state = request.form.get('state')
    district = request.form.get('district')

    # Query the database and filter based on state and optionally district
    with engine.connect() as connection:
        query = f"SELECT * FROM health_data WHERE State = '{state}'"
        if district:
            query += f" AND District = '{district}'"
        filtered_data = pd.read_sql(query, connection)

    # Extract relevant columns for map data
    map_data = filtered_data[['District', 'Latitude', 'Longitude', 'Target (Healthcare Access)']]
    map_data.columns = ['district', 'latitude', 'longitude', 'healthcare_access']

    # Convert to dictionary format for JSON response
    result = map_data.to_dict(orient='records')

    return jsonify({'data': result})

# Route to download CSV report
@app.route('/download-report', methods=['GET'])
@login_required
def download_report():
    # Fetch filters from request args
    filters = {
        'state': request.args.get('state'),
        'district': request.args.get('district'),
        'tb_incidence': request.args.get('tb_incidence'),
        'diabetes': request.args.get('diabetes'),
        'malaria_incidence': request.args.get('malaria_incidence'),
        'hiv_aids': request.args.get('hiv_aids'),
        'imr': request.args.get('imr'),
        'vaccination': request.args.get('vaccination'),
        'income': request.args.get('income'),
        'employment_rate': request.args.get('employment_rate'),
        'education': request.args.get('education'),
        'housing': request.args.get('housing'),
        'urbanization': request.args.get('urbanization'),
        'aqi': request.args.get('aqi'),
        'annual_rainfall': request.args.get('annual_rainfall'),
        'healthcare_access': request.args.get('healthcare_access')
    }

    # Filter the HealthData based on filters
    filtered_data = HealthData.query  # Start with all data

    if filters['state']:
        filtered_data = filtered_data.filter(HealthData.state == filters['state'])
    if filters['district']:
        filtered_data = filtered_data.filter(HealthData.district == filters['district'])
    if filters['tb_incidence']:
        filtered_data = filtered_data.filter(HealthData.tb_incidence >= filters['tb_incidence'])
    if filters['diabetes']:
        filtered_data = filtered_data.filter(HealthData.diabetes >= filters['diabetes'])
    if filters['malaria_incidence']:
        filtered_data = filtered_data.filter(HealthData.malaria_incidence >= filters['malaria_incidence'])
    if filters['hiv_aids']:
        filtered_data = filtered_data.filter(HealthData.hiv_aids >= filters['hiv_aids'])
    if filters['imr']:
        filtered_data = filtered_data.filter(HealthData.imr >= filters['imr'])
    if filters['vaccination']:
        filtered_data = filtered_data.filter(HealthData.vaccination >= filters['vaccination'])
    if filters['income']:
        filtered_data = filtered_data.filter(HealthData.income >= filters['income'])
    if filters['employment_rate']:
        filtered_data = filtered_data.filter(HealthData.employment_rate >= filters['employment_rate'])
    if filters['education']:
        filtered_data = filtered_data.filter(HealthData.education >= filters['education'])
    if filters['housing']:
        filtered_data = filtered_data.filter(HealthData.housing >= filters['housing'])
    if filters['urbanization']:
        filtered_data = filtered_data.filter(HealthData.urbanization >= filters['urbanization'])
    if filters['aqi']:
        filtered_data = filtered_data.filter(HealthData.aqi >= filters['aqi'])
    if filters['annual_rainfall']:
        filtered_data = filtered_data.filter(HealthData.annual_rainfall >= filters['annual_rainfall'])
    if filters['healthcare_access']:
        filtered_data = filtered_data.filter(HealthData.healthcare_access >= filters['healthcare_access'])

    data = filtered_data.all()  # Fetch the filtered data

    # Prepare CSV response
    output = []
    for row in data:
        output.append([row.state, row.district, row.tb_incidence, row.diabetes, row.malaria_incidence,
                       row.hiv_aids, row.imr, row.vaccination, row.income, row.employment_rate,
                       row.education, row.housing, row.urbanization, row.aqi, row.annual_rainfall,
                       row.healthcare_access])

    output_df = pd.DataFrame(output, columns=['State', 'District', 'TB Incidence', 'Diabetes', 
                                               'Malaria Incidence', 'HIV/AIDS', 'IMR', 'Vaccination',
                                               'Income', 'Employment Rate', 'Education', 'Housing',
                                               'Urbanization', 'AQI', 'Annual Rainfall', 'Healthcare Access'])

    # Create CSV response
    response = make_response(output_df.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment; filename=health_report.csv"
    response.headers["Content-type"] = "text/csv"

    return response  # Returns the CSV file to download

# Route to download PDF report
@app.route('/download-report/pdf', methods=['GET'])
@login_required
def download_report_pdf():
    # Fetch filters from request args
    filters = {
        'state': request.args.get('state'),
        'district': request.args.get('district'),
        'tb_incidence': request.args.get('tb_incidence'),
        'diabetes': request.args.get('diabetes'),
        'malaria_incidence': request.args.get('malaria_incidence'),
        'hiv_aids': request.args.get('hiv_aids'),
        'imr': request.args.get('imr'),
        'vaccination': request.args.get('vaccination'),
        'income': request.args.get('income'),
        'employment_rate': request.args.get('employment_rate'),
        'education': request.args.get('education'),
        'housing': request.args.get('housing'),
        'urbanization': request.args.get('urbanization'),
        'aqi': request.args.get('aqi'),
        'annual_rainfall': request.args.get('annual_rainfall'),
        'healthcare_access': request.args.get('healthcare_access')
    }

    # Filter the HealthData based on filters
    filtered_data = HealthData.query  # Start with all data

    if filters['state']:
        filtered_data = filtered_data.filter(HealthData.state == filters['state'])
    if filters['district']:
        filtered_data = filtered_data.filter(HealthData.district == filters['district'])
    if filters['tb_incidence']:
        filtered_data = filtered_data.filter(HealthData.tb_incidence >= filters['tb_incidence'])
    if filters['diabetes']:
        filtered_data = filtered_data.filter(HealthData.diabetes >= filters['diabetes'])
    if filters['malaria_incidence']:
        filtered_data = filtered_data.filter(HealthData.malaria_incidence >= filters['malaria_incidence'])
    if filters['hiv_aids']:
        filtered_data = filtered_data.filter(HealthData.hiv_aids >= filters['hiv_aids'])
    if filters['imr']:
        filtered_data = filtered_data.filter(HealthData.imr >= filters['imr'])
    if filters['vaccination']:
        filtered_data = filtered_data.filter(HealthData.vaccination >= filters['vaccination'])
    if filters['income']:
        filtered_data = filtered_data.filter(HealthData.income >= filters['income'])
    if filters['employment_rate']:
        filtered_data = filtered_data.filter(HealthData.employment_rate >= filters['employment_rate'])
    if filters['education']:
        filtered_data = filtered_data.filter(HealthData.education >= filters['education'])
    if filters['housing']:
        filtered_data = filtered_data.filter(HealthData.housing >= filters['housing'])
    if filters['urbanization']:
        filtered_data = filtered_data.filter(HealthData.urbanization >= filters['urbanization'])
    if filters['aqi']:
        filtered_data = filtered_data.filter(HealthData.aqi >= filters['aqi'])
    if filters['annual_rainfall']:
        filtered_data = filtered_data.filter(HealthData.annual_rainfall >= filters['annual_rainfall'])
    if filters['healthcare_access']:
        filtered_data = filtered_data.filter(HealthData.healthcare_access >= filters['healthcare_access'])

    data = filtered_data.all()  # Fetch the filtered data

    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)

    # Add table headers
    headers = ['State', 'District', 'TB Incidence', 'Diabetes', 'Malaria Incidence', 'HIV/AIDS', 
               'IMR', 'Vaccination', 'Income', 'Employment Rate', 'Education', 'Housing',
               'Urbanization', 'AQI', 'Annual Rainfall', 'Healthcare Access']
    for header in headers:
        pdf.cell(30, 10, header, 1)
    pdf.ln()  # New line after header row

    # Add data rows to the PDF
    pdf.set_font("Arial", '', 12)
    for row in data:
        pdf.cell(30, 10, row.state, 1)
        pdf.cell(30, 10, row.district, 1)
        pdf.cell(30, 10, str(row.tb_incidence), 1)
        pdf.cell(30, 10, str(row.diabetes), 1)
        pdf.cell(30, 10, str(row.malaria_incidence), 1)
        pdf.cell(30, 10, str(row.hiv_aids), 1)
        pdf.cell(30, 10, str(row.imr), 1)
        pdf.cell(30, 10, str(row.vaccination), 1)
        pdf.cell(30, 10, str(row.income), 1)
        pdf.cell(30, 10, str(row.employment_rate), 1)
        pdf.cell(30, 10, str(row.education), 1)
        pdf.cell(30, 10, str(row.housing), 1)
        pdf.cell(30, 10, str(row.urbanization), 1)
        pdf.cell(30, 10, str(row.aqi), 1)
        pdf.cell(30, 10, str(row.annual_rainfall), 1)
        pdf.cell(30, 10, str(row.healthcare_access), 1)
        pdf.ln()  # New line after each row

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers["Content-Disposition"] = "attachment; filename=health_report.pdf"
    response.headers["Content-type"] = "application/pdf"

    return response  # Returns the PDF file to download

# Route to handle resources
@app.route('/resources')
def resources():
    resources = Resource.query.all()  # Fetch all resources from the database
    return render_template('resources.html', resources=resources)

if __name__ == '__main__':
    app.run(debug=True)