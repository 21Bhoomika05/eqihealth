import pandas as pd
from .models import HealthData
from . import db

def load_data_from_csv(csv_file):
    data = pd.read_csv(csv_file)

    for index, row in data.iterrows():
        health_data = HealthData(
            state=row['State'],
            district=row['District'],
            latitude=row['Latitude'],
            longitude=row['Longitude'],
            tb_incidence=row['TB Incidence'],
            diabetes=row['Diabetes'],
            malaria=row['Malaria Incidence'],
            hiv_aids=row['HIV/AIDS'],
            imr=row['MMR'],
            vaccination=row['Vaccination'],
            income_level=row['Income Level'],
            education=row['Education'],
            housing_conditions=row['Housing Conditions'],
            urbanization=row['Urbanization'],
            aqi=row['AQI'],
            annual_rainfall=row['Annual Rainfall'],
            target_healthcare_access=row['Target Healthcare Access']
        )
        db.session.add(health_data)

    db.session.commit()