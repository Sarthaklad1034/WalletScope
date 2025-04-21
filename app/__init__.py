from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    from app.routes.auth import auth
    from app.routes.expenses import expenses
    from app.routes.budget import budget
    from app.routes.dashboard import dashboard
    
    app.register_blueprint(auth)
    app.register_blueprint(expenses)
    app.register_blueprint(budget)
    app.register_blueprint(dashboard)
    
    with app.app_context():
        db.create_all()
        
    return app