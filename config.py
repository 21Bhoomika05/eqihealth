import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Base directory of the app
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "database.db")}')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
