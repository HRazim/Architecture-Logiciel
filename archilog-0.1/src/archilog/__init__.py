import os
from dataclasses import dataclass
from flask import Flask

@dataclass
class Config:
    DATABASE_URL: str
    DEBUG: bool
    SECRET_KEY: str

# Configuration par défaut
config = Config(
    DATABASE_URL=os.getenv("ARCHILOG_DATABASE_URL", "sqlite:///data.db"),
    DEBUG=os.getenv("ARCHILOG_DEBUG", "False") == "True",
    SECRET_KEY=os.getenv("ARCHILOG_FLASK_SECRET_KEY", "your_secret_key_here")
)

def create_app():
    """Application factory pour créer l'application Flask"""
    app = Flask(__name__)
    
    # Configuration de Flask avec le préfixe ARCHILOG_FLASK
    app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")
    app.secret_key = config.SECRET_KEY
    
    # Enregistrement des blueprints
    from archilog.blueprints.web_ui import web_ui
    from archilog.blueprints.api import api
    
    app.register_blueprint(web_ui)
    app.register_blueprint(api)
    
    # Configuration des gestionnaires d'erreurs
    from archilog.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app