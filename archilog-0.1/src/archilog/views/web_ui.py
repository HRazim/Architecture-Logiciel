import uuid
import io
import logging

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_wtf import FlaskForm

from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import archilog.models as models
import archilog.services as services


# Initialisation de l'authentification HTTP
auth = HTTPBasicAuth()

# Configuration des utilisateurs et des rôles
users = {
    "admin": {
        "roles": ["admin"],
        "password": generate_password_hash("admin")
    },
    "user": {
        "roles": ["user"],
        "password": generate_password_hash("user")
    }
}

@auth.verify_password
def verify_password(username, password):
    """Vérification des identifiants de connexion"""
    if username in users and check_password_hash(users[username]['password'], password):
        return username
    return None

@auth.get_user_roles
def get_user_roles(username):
    """Récupération des rôles d'un utilisateur"""
    return users[username]['roles'] if username in users else []



# Formulaire de Validation
class EntryForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(message="Le nom est obligatoire")])
    amount = FloatField("Montant", validators=[
        DataRequired(message="Le montant est obligatoire"),
        NumberRange(min=0, message="Le montant doit être positif")
    ])
    category = StringField("Catégorie", validators=[Optional()])
    submit = SubmitField("Enregistrer")




# Création du blueprint pour l'interface web
web_ui = Blueprint("web_ui", __name__, url_prefix="/")

# Route d'accueil protégée
@web_ui.route('/')
@auth.login_required
def home():
    try:
        entries = models.get_all_entries()
        return render_template('home.html', entries=entries, username=auth.current_user())
    except Exception as e:
        logging.exception("Erreur lors de la récupération des entrées")
        flash(f"Erreur: {str(e)}", "error")
        return render_template('home.html', entries=[])

# Routes protégées avec différents niveaux d'accès
@web_ui.route('/create', methods=['GET', 'POST'])
@auth.login_required(role=['admin'])
def create_entry():
    form = EntryForm()
    
    if form.validate_on_submit():
        try:
            models.create_entry(form.name.data, form.amount.data, form.category.data or None)
            logging.info(f"Nouvelle entrée créée: {form.name.data}")
            flash('Entrée créée avec succès!', 'success')
            return redirect(url_for('web_ui.home'))
        except Exception as e:
            logging.exception(f"Erreur lors de la création d'une entrée")
            flash(f'Erreur lors de la création: {str(e)}', 'error')

    return render_template('create.html', form=form)

@web_ui.route('/update/<uuid:id>', methods=['GET', 'POST'])
@auth.login_required(role=['admin'])
def update_entry(id):
    try:
        entry = models.get_entry(id)
        form = EntryForm(obj=entry)

        if form.validate_on_submit():
            models.update_entry(id, form.name.data, form.amount.data, form.category.data or None)
            logging.info(f"Entrée mise à jour: {id}")
            flash('Entrée mise à jour avec succès !', 'success')
            return redirect(url_for('web_ui.home'))

        return render_template('update.html', form=form, entry=entry)
    except Exception as e:
        logging.exception(f"Erreur lors de la mise à jour de l'entrée {id}")
        flash(f'Erreur: {str(e)}', 'error')
        return redirect(url_for('web_ui.home'))

@web_ui.route('/delete/<uuid:id>', methods=['GET', 'POST'])
@auth.login_required(role=['admin'])
def delete_entry(id):
    try:
        models.delete_entry(id)
        logging.info(f"Entrée supprimée: {id}")
        flash('Entrée supprimée avec succès!', 'success')
    except Exception as e:
        logging.exception(f"Erreur lors de la suppression de l'entrée {id}")
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')

    return redirect(url_for('web_ui.home'))

@web_ui.route('/export-csv')
@auth.login_required(role=['admin'])
def export_csv():
    try:
        csv_content = services.export_to_csv().getvalue()
        logging.info("Exportation CSV réussie")
        return csv_content, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=entries.csv'
        }
    except Exception as e:
        logging.exception("Erreur lors de l'exportation CSV")
        flash(f'Erreur lors de l\'exportation: {str(e)}', 'error')
        return redirect(url_for('web_ui.home'))

@web_ui.route('/import-csv', methods=['POST'])
@auth.login_required(role=['admin'])
def import_csv():
    if 'csv_file' not in request.files:
        logging.warning("Tentative d'import CSV sans fichier")
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('web_ui.home'))

    file = request.files['csv_file']

    if file.filename == '':
        logging.warning("Tentative d'import CSV avec un nom de fichier vide")
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('web_ui.home'))

    if file and file.filename.endswith('.csv'):
        try:
            stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
            services.import_from_csv(stream)
            logging.info("Importation CSV réussie")
            flash('Fichier CSV importé avec succès !', 'success')
        except Exception as e:
            logging.exception("Erreur lors de l'importation CSV")
            flash(f'Erreur lors de l\'importation : {str(e)}', 'error')
    else:
        logging.warning(f"Tentative d'import avec un fichier non CSV: {file.filename}")
        flash('Le fichier doit être un CSV', 'error')

    return redirect(url_for('web_ui.home'))
