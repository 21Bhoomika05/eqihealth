from flask import jsonify
from .models import HealthData

def get_all_health_data():
    data = HealthData.query.all()
    return jsonify([{
        'state': d.state,
        'district': d.district,
        'latitude': d.latitude,
        'longitude': d.longitude,
        'tb_incidence': d.tb_incidence,
        'diabetes': d.diabetes,
        'malaria_incidence': d.malaria,
        'hiv_aids': d.hiv_aids,
        'imr': d.imr,
        'vaccination': d.vaccination,
        'income_level': d.income_level,
        'education': d.education,
        'housing_conditions': d.housing_conditions,
        'urbanization': d.urbanization,
        'aqi': d.aqi,
        'annual_rainfall': d.annual_rainfall,
        'target_healthcare_access': d.target_healthcare_access
    } for d in data])