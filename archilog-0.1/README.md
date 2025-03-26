# Archilog

A simple project for educational purpose.


# Sommaire

1. [Introduction](#archilog)
2. [Technologies utilisées](#technologies-utilisées)
   - [SQLAlchemy Core](#sqlalchemy-core)
   - [Flask](#flask)
   - [Jinja2](#jinja2)
    - [WTForms](#wtforms)
3. [Structure du projet](#structure-du-projet)
4. [Commandes disponibles](#commandes-disponibles)
5. [Fonctionnalités](#fonctionnalités)
6. [Installation](#installation)
7. [Utilisation](#utilisation)
   - [Interface en ligne de commande](#interface-en-ligne-de-commande)
   - [Interface web](#interface-web)
8. [Développement](#développement)
   - [Modèles de données (models.py)](#modèles-de-données-models-py)
   - [Services (services.py)](#services-services-py)
   - [Blueprints](#blueprints)
9. [Industrialisation](#industrialisation)
   - [Modularité : Blueprints](#modularité--blueprints)
   - [Modularité : Application Factory](#modularité--application-factory)
   - [Configuration centralisée](#configuration-centralisée)
   - [Utilisation de dotenv](#utilisation-de-dotenv)
   - [Gestion des erreurs](#gestion-des-erreurs)
10. [Validation & Traçabilité](#validation--traçabilité)
    - [Types de validation](#types-de-validation)
    - [WTForms](#wtforms)
    - [Logging](#logging)
11. [Ressources](#ressources)


## Technologies utilisées

### SQLAlchemy Core

SQLAlchemy est un toolkit SQL et un ORM (Object-Relational Mapping) écrit en Python. Dans ce projet, nous utilisons uniquement SQLAlchemy Core (pas l'ORM) pour interagir avec la base de données SQLite.

```python
from sqlalchemy import create_engine, Table, MetaData, Column, String, Float

# Connexion à la base SQLite
engine = create_engine('sqlite:///data.db')
metadata = MetaData()

# Définition de la table 'entries'
entries = Table(
    'entries',
    metadata,
    Column('id', String, primary_key=True),
    Column('name', String, nullable=False),
    Column('amount', Float, nullable=False),
    Column('category', String, nullable=True)
)
```

Exemple d'utilisation : 

- Cette table stocke les entrées financières avec un identifiant unique, un nom, un montant et une catégorie optionnelle.

### Flask

Flask est un framework web léger pour Python, parfait pour créer rapidement une interface web. Dans Archilog, il sert à afficher les entrées et à gérer les interactions utilisateur via des formulaires.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    entries = models.get_all_entries()
    return render_template('home.html', entries=entries)
```

Exemple d'utilisation : 

- La route racine récupère toutes les entrées et les affiche via un template HTML.

### Jinja2

Jinja2, intégré à Flask, génère des pages HTML dynamiques en combinant des templates avec les données de l'application.

```html
{% if entries and entries|length > 0 %}
    <table>
        {% for entry in entries %}
            <tr>
                <td>{{ entry.id }}</td>
                <td>{{ entry.name }}</td>
            </tr>
        {% endfor %}
    </table>
{% endif %}
```

### WTForms

WTForms est une bibliothèque de validation de formulaires pour Flask qui permet de définir et de valider des formulaires de manière robuste.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class EntryForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(message="Le nom est obligatoire")])
    amount = FloatField("Montant", validators=[
        DataRequired(message="Le montant est obligatoire"),
        NumberRange(min=0, message="Le montant doit être positif")
    ])
    category = StringField("Catégorie", validators=[Optional()])
    submit = SubmitField("Enregistrer")
```


## Structure du projet

```
.
├── dev.env                    # Configuration environnement de développement
├── pyproject.toml
├── README.md
└── src
    └── archilog
        ├── __init__.py           # Configuration centralisée 
        ├── views                 # Organisation Web modulaire avec blueprints
        │   ├── __init__.py       # Configuration Web 
        │   ├── static
        │   └── css
        │       └── style.css     # Styles CSS
        ├── templates
        │   ├── create.html       # Formulaire de création
        │   ├── errors            # Templates pour pages d'erreur
        │   │   ├── 404.html      # Page non trouvée
        │   │   └── 500.html      # Erreur serveur
        │   ├── home.html         # Page d'accueil
        │   └── update.html       # Formulaire de modification
        │   ├── api.py            # Blueprint pour l'API et CLI
        │   ├── error_handlers.py # Gestionnaires d'erreurs centralisés
        │   ├── forms.py          # Form validation
        │   └── web_ui.py         # Blueprint pour l'interface web
        │
        ├── models.py             # Modèles de données et fonctions d'accès à la BDD
        ├── services.py           # Services d'import/export CSV
        
```

## Commandes disponibles

```bash
$ pdm run flask --app archilog:create_app archilog
Usage: flask archilog [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create      Créer une nouvelle entrée
  delete      Supprimer une entrée existante
  get         Récupérer une entrée par son ID
  get-all     Lister toutes les entrées (avec option CSV)
  import-csv  Importer des données depuis un fichier CSV
  init-db     Initialiser la base de données
  update      Mettre à jour une entrée existante
```

Exemples :

- `pdm run flask --app archilog:create_app archilog create` : Demande les détails (nom, montant, catégorie) pour une nouvelle entrée.
- `pdm run flask --app archilog:create_app archilog get-all --as-csv` : Exporte toutes les entrées au format CSV.

## Fonctionnalités

- Affichage de toutes les entrées financières
- Création, modification et suppression d'entrées
- Importation et exportation de données au format CSV
- Interface web intuitive
- Gestion des erreurs avec messages flash
- Interface en ligne de commande complète
- Architecture modulaire avec blueprints
- Configuration centralisée avec dotenv
- Gestion d'erreurs avancée

## Installation

1. Installez les dépendances avec PDM:
   ```
   pdm add flask sqlalchemy python-dotenv
   ```

2. Créez un fichier `dev.env` à la racine du projet:
   ```
   ARCHILOG_DATABASE_URL=sqlite:///data.db
   ARCHILOG_DEBUG=True
   ARCHILOG_FLASK_SECRET_KEY=your_secret_key_here
   ```

3. Initialisez la base de données:
   ```
   pdm run flask --app archilog.views:create_app archilog init-db
   ```

## Utilisation

### Interface en ligne de commande

```bash
# Créer une entrée
pdm run flask --app archilog.views:create_app archilog create
# Entrer : name="Salaire", amount=1500, category="Revenus"

# Afficher toutes les entrées
pdm run flask --app archilog.views:create_app archilog get-all

# Exporter au format CSV
pdm run flask --app archilog.views:create_app archilog get-all --as-csv > export.csv

# Importer depuis un CSV
pdm run flask --app archilog.views:create_app archilog import-csv export.csv

# Récupérer une entrée par son ID
pdm run flask --app archilog.views:create_app archilog get --id <UUID>

# Mettre à jour une entrée
pdm run flask --app archilog.views:create_app archilog update --id <UUID>

# Supprimer une entrée
pdm run flask --app archilog.views:create_app archilog delete --id <UUID>
```

### Interface web

Lancez l'application Flask:
```
pdm run start
```

Puis ouvrez http://localhost:5000 dans votre navigateur.

## Développement

### Modèles de données (models.py)

Le module `models.py` définit la structure de la base de données et fournit des fonctions pour :
- Initialiser la base de données
- Créer, lire, mettre à jour et supprimer des entrées
- Gérer les connexions à la base de données avec un gestionnaire de contexte

### Services (services.py)

Le module `services.py` contient des fonctions utilitaires pour :
- Exporter les données au format CSV
- Importer des données depuis un fichier CSV

### Blueprints

Les blueprints permettent d'organiser l'application en modules réutilisables :
- `web_ui.py` : Gère l'interface utilisateur web
- `api.py` : Gère l'API et les commandes CLI

## Industrialisation

### Modularité : Blueprints

Les blueprints Flask permettent de structurer l'application en modules :

```python
from flask import Blueprint, render_template

web_ui = Blueprint("web_ui", __name__, url_prefix="/")

@web_ui.route("/<page>")
def show(page):
    return render_template(f"pages/{page}.html")
```

### Modularité : Application Factory

L'application factory permet de créer l'application Flask de manière dynamique, facilitant les tests et la maintenance :

```python
def create_app():
    app = Flask(__name__)

    from archilog.blueprints.api import api
    from archilog.blueprints.web_ui import web_ui
    app.register_blueprint(api)
    app.register_blueprint(web_ui)

    return app
```

Pour lancer l'application, il suffit d'exécuter :

```
$ pdm run flask --app archilog:create_app --debug run
```

### Configuration centralisée

Avant, la configuration était éparpillée :

```python
engine = create_engine("sqlite:///data.db", echo=True)
metadata = MetaData()
```

Maintenant, nous utilisons une configuration centralisée :

```python
from archilog import config

engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
metadata = MetaData()
```

Définie dans `src/archilog/__init__.py` :

```python
from dataclasses import dataclass

@dataclass
class Config:
    DATABASE_URL: str
    DEBUG: bool
    SECRET_KEY: str

config = Config(
    DATABASE_URL="sqlite:///data.db",
    DEBUG=True,
    SECRET_KEY="your_secret_key_here"
)
```

### Utilisation de dotenv

Pour chaque environnement, nous pouvons avoir une configuration spécifique :
* `dev.env` : Développement
* `testing.env` : Tests
* `demo.env` : Démonstration
* `prod.env` : Production

Format du fichier `dev.env` :

```
ARCHILOG_DATABASE_URL=sqlite:///data.db
ARCHILOG_DEBUG=True
ARCHILOG_FLASK_SECRET_KEY=secret!
```

Utilisation avec PDM dans `pyproject.toml` :

```toml
[tool.pdm.scripts]
_.env_file = "dev.env"
start = "flask --app archilog.views:create_app --debug run"
```

Intégration dans l'application :

```python
import os

config = Config(
    DATABASE_URL=os.getenv("ARCHILOG_DATABASE_URL", ""),
    DEBUG=os.getenv("ARCHILOG_DEBUG", "False") == "True",
    SECRET_KEY=os.getenv("ARCHILOG_FLASK_SECRET_KEY", "default_key")
)
```

Configuration Flask avec préfixe :

```python
app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")
```

### Gestion des erreurs

Nous avons amélioré la gestion des erreurs avec des handlers spécifiques :

```python
@app.errorhandler(500)
def handle_internal_error(error):
    flash("Erreur interne du serveur", "error")
    return render_template("errors/500.html"), 500
```

Les erreurs peuvent être déclenchées via :

```python
from flask import abort

@web_ui.route('/error-test')
def error_test():
    abort(500)  # Déclenche une erreur 500
```

## Validation & Traçabilité

### Types de validation

Nous utilisons deux types principaux de validation des données :

1. **Validation Syntaxique** : 
   - Vérification du type de données (date, entier, texte, etc.)
   - Assure que les données sont du format attendu
   - Exemple : Un champ de montant doit être un nombre décimal

2. **Validation Sémantique** : 
   - Vérification de la cohérence et du sens des données
   - Exemple : Un montant doit être supérieur à zéro
   - Exemple : Un nom ne peut pas être vide

### WTForms

Dans Archilog, WTForms est utilisé pour valider les formulaires d'entrée :

```python
@web_ui.route('/create', methods=['GET', 'POST'])
def create_entry():
    form = EntryForm()
    
    if form.validate_on_submit():
        try:
            # Création de l'entrée avec les données validées
            models.create_entry(
                form.name.data, 
                form.amount.data, 
                form.category.data or None
            )
            logging.info(f"Nouvelle entrée créée: {form.name.data}")
            flash('Entrée créée avec succès!', 'success')
            return redirect(url_for('web_ui.home'))
        except Exception as e:
            logging.exception(f"Erreur lors de la création d'une entrée")
            flash(f'Erreur lors de la création: {str(e)}', 'error')

    return render_template('create.html', form=form)
```

Les validations incluent :
- `DataRequired()` : Champs obligatoires
- `NumberRange(min=0)` : Validation de valeurs numériques
- `Optional()` : Champs facultatifs
- Messages d'erreur personnalisés

### Logging

Configuration et utilisation du logging pour le suivi et le débogage :

```python
import logging
from flask import current_app

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("archilog.log"),
        logging.StreamHandler()
    ]
)

 @app.errorhandler(500)
    def handle_internal_error(error):
        logging.exception("Erreur interne du serveur")
        flash("Erreur interne du serveur", "error")
        return render_template("errors/500.html"), 500

# Exemple de log durant l'exécution
def create_entry():
    logging.info(f"Nouvelle entrée créée: {form.name.data}")
    #reste du code
```

## Installation

```bash
$ uv add flask-wtf
```

## Ressources

- Documentation SQLAlchemy
- Documentation Flask
- Documentation Jinja2
- Documentation Blueprints : https://flask.palletsprojects.com/en/3.0.x/blueprints/
- Documentation Application Factory : https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
- Documentation PDM Scripts : https://pdm.fming.dev/latest/usage/scripts/
- Documentation Gestion des erreurs : https://flask.palletsprojects.com/en/3.0.x/errorhandling/#error-handlers
- Documentation WTForms : https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/
- Documentation Flask-WTF : https://flask-wtf.readthedocs.io/
- Validation de formulaires Python : https://wtforms.readthedocs.io/
- Cours et exemples : [https://kathode.neocities.org](https://kathode.neocities.org)