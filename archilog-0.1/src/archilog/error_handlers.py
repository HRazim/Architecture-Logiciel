from flask import flash, redirect, url_for, render_template

def register_error_handlers(app):
    """Enregistre tous les gestionnaires d'erreur pour l'application"""
    
    @app.errorhandler(404)
    def handle_not_found(error):
        flash("Page non trouvée", "error")
        return render_template("errors/404.html"), 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        flash("Erreur interne du serveur", "error")
        return render_template("errors/500.html"), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        flash(f"Une erreur inattendue s'est produite: {str(error)}", "error")
        return redirect(url_for("web_ui.home"))  # Laissez tel quel ici, car hors contexte blueprint