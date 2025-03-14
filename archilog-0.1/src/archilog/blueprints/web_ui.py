import uuid
import io
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

import archilog.models as models
import archilog.services as services

# Création du blueprint pour l'interface web
web_ui = Blueprint("web_ui", __name__, url_prefix="/")

@web_ui.route('/')
def home():
    try:
        entries = models.get_all_entries()
        return render_template('home.html', entries=entries)
    except Exception as e:
        flash(f"Erreur: {str(e)}", "error")
        return render_template('home.html', entries=[])

@web_ui.route('/create', methods=['GET', 'POST'])
def create_entry():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category'] or None

        try:
            models.create_entry(name, amount, category)
            flash('Entrée créée avec succès!', 'success')
            return redirect(url_for('web_ui.home'))
        except Exception as e:
            flash(f'Erreur lors de la création: {str(e)}', 'error')

    return render_template('create.html')

@web_ui.route('/update/<uuid:id>', methods=['GET', 'POST'])
def update_entry(id):
    try:
        entry = models.get_entry(id)

        if request.method == 'POST':
            name = request.form['name']
            amount = float(request.form['amount'])
            category = request.form['category'] or None

            models.update_entry(id, name, amount, category)
            flash('Entrée mise à jour avec succès !', 'success')
            return redirect(url_for('web_ui.home'))

        return render_template('update.html', entry=entry)
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
        return redirect(url_for('web_ui.home'))

@web_ui.route('/delete/<uuid:id>', methods=['GET', 'POST'])
def delete_entry(id):
    try:
        models.delete_entry(id)
        flash('Entrée supprimée avec succès!', 'success')
    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')

    return redirect(url_for('web_ui.home'))

@web_ui.route('/export-csv')
def export_csv():
    try:
        csv_content = services.export_to_csv().getvalue()
        return csv_content, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=entries.csv'
        }
    except Exception as e:
        flash(f'Erreur lors de l\'exportation: {str(e)}', 'error')
        return redirect(url_for('web_ui.home'))

@web_ui.route('/import-csv', methods=['POST'])
def import_csv():
    if 'csv_file' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('web_ui.home'))

    file = request.files['csv_file']

    if file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('web_ui.home'))

    if file and file.filename.endswith('.csv'):
        try:
            stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
            services.import_from_csv(stream)
            flash('Fichier CSV importé avec succès !', 'success')
        except Exception as e:
            flash(f'Erreur lors de l\'importation : {str(e)}', 'error')
    else:
        flash('Le fichier doit être un CSV', 'error')

    return redirect(url_for('web_ui.home'))

# Page d'exemple pour tester la gestion des erreurs
@web_ui.route('/error-test')
def error_test():
    abort(500)  # Déclenche volontairement une erreur 500