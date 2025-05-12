from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from habit_tracker.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Registrar blueprints aqui
    
    return app
