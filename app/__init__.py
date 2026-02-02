# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth
    from app.routes.chat import chat
    from app.routes.message import message
    
    app.register_blueprint(auth)
    app.register_blueprint(chat)
    app.register_blueprint(message)
    
    with app.app_context():
        db.create_all()
        
    return app