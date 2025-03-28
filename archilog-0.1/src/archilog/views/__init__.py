from flask import Flask
from flask_httpauth import HTTPBasicAuth

def create_app():
    """Application factory pour créer l'application Flask"""
    # Configuration du logging
    
    app = Flask(__name__)
    auth = HTTPBasicAuth()
    
    # Configuration de Flask avec le préfixe ARCHILOG_FLASK
    app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")
    
    # Enregistrement des blueprints
    from archilog.views.web_ui import web_ui
    from archilog.views.api import api
    from archilog.views.api_views import api_views, spec, register_spec
    
    app.register_blueprint(web_ui)
    app.register_blueprint(api)
    app.register_blueprint(api_views)
    
    # Enregistrement du schéma Spectree
    register_spec(app)
    
    # Configuration des gestionnaires d'erreurs
    from archilog.views.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    return app