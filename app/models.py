from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user (primary key)
    username = db.Column(db.String(150), nullable=False, unique=True)  # Username must be unique
    email = db.Column(db.String(150), unique=True)  # Email must also be unique
    password = db.Column(db.String(150))  # Password stored as a hashed string

class Resource(db.Model):
    _tablename_ = 'resources'  # Define the table name for resources

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each resource (primary key)
    title = db.Column(db.String(200), nullable=False)  # Title of the resource
    url = db.Column(db.String(500), nullable=False)  # URL for the resource

    def _repr_(self):
        return f'<Resource {self.title}>'

class HealthData(db.Model):
    _tablename_ = 'health_statistics'  

    id = db.Column(db.Integer, primary_key=True) 
    state = db.Column(db.String(100), nullable=False)  
    district = db.Column(db.String(100), nullable=False)  
    latitude = db.Column(db.Float, nullable=False)  
    longitude = db.Column(db.Float, nullable=False)  
    tb_incidence = db.Column(db.Float)  
    diabetes = db.Column(db.Float)  
    malaria_incidence = db.Column(db.Float)  
    hiv_aids = db.Column(db.Float)  
    imr = db.Column(db.Float) 
    vaccination = db.Column(db.Float)  
    income_level = db.Column(db.Float)  
    education = db.Column(db.Float)  
    housing_conditions = db.Column(db.Float)  
    urbanization = db.Column(db.Float)  
    aqi = db.Column(db.Float)  
    annual_rainfall = db.Column(db.Integer)  
    target_healthcare_access = db.Column(db.Integer)  
    def _repr_(self):
        return f'<HealthData {self.state} - {self.district}>'