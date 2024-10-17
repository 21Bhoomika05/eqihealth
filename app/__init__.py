from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config 

# Initialize extensions
db = SQLAlchemy()  
migrate = Migrate()  
login_manager = LoginManager()  

# Configure the login manager to handle user authentication routes
login_manager.login_view = 'auth.login'  
login_manager.login_message_category = 'info'  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .routes import main_bp  
    app.register_blueprint(main_bp)  

    from .auth import auth_bp  
    app.register_blueprint(auth_bp)  


    with app.app_context():
        from .models import User, HealthData 
        db.create_all()  

    return app

if __name__ == '__main__':
    app = create_app()  
    app.run(debug=True)  