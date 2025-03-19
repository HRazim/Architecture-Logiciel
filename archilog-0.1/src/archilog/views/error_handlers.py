import logging
from flask import flash, redirect, url_for, render_template

def register_error_handlers(app):
    """Enregistre tous les gestionnaires d'erreur pour l'application"""
    
    @app.errorhandler(404)
    def handle_not_found(error):
        logging.warning(f"Page non trouvée")
        flash("Page non trouvée", "error")
        return render_template("errors/404.html"), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        logging.exception("Erreur interne du serveur")
        flash("Erreur interne du serveur", "error")
        return render_template("errors/500.html"), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logging.exception(f"Exception non gérée: {str(error)}")
        flash(f"Une erreur inattendue s'est produite: {str(error)}", "error")
        return redirect(url_for("web_ui.home"))