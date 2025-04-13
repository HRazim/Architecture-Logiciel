# Archilog

Un projet éducatif complet combinant CLI, gestion de données et interface web avec une API HTTP.

## Vue d'ensemble

Archilog est une application Python modulaire et évolutive qui démontre l'implémentation de bonnes pratiques de développement à travers la gestion d'entrées financières. Elle propose trois modes d'interaction:

- Une interface en ligne de commande (CLI)
- Une interface web responsive
- Une API HTTP RESTful documentée

## Technologies utilisées

### SQLAlchemy Core
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

### Flask
Framework web léger pour créer l'interface utilisateur et l'API, organisé en blueprints:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    entries = models.get_all_entries()
    return render_template('home.html', entries=entries)
```

### Jinja2
Moteur de templates pour générer des pages HTML dynamiques:
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
Bibliothèque de validation de formulaires pour Flask:
```python
class EntryForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(message="Le nom est obligatoire")])
    amount = FloatField("Montant", validators=[
        DataRequired(message="Le montant est obligatoire"),
        NumberRange(min=0, message="Le montant doit être positif")
    ])
    category = StringField("Catégorie", validators=[Optional()])
    submit = SubmitField("Enregistrer")
```

### Flask-HTTPAuth
Extension Flask pour l'authentification HTTP et le contrôle d'accès:
```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
       check_password_hash(users.get(username), password):
        return username
```

### Spectree et Pydantic
Outils pour la validation d'API et la génération de documentation OpenAPI:
```python
from spectree import SpecTree, SecurityScheme
from pydantic import BaseModel, Field

spec = SpecTree(
    "flask", 
    title="ArchiLog API",
    version="1.0.0"
)

class EntryModel(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    amount: float = Field(gt=0)
    category: str | None = Field(default=None)
```

## Structure du projet

```
.
├── dev.env                  # Configuration environnement de développement
├── pyproject.toml
├── README.md
└── src
    └── archilog
        ├── __init__.py         # Configuration centralisée 
        ├── models.py           # Modèles et accès BDD
        ├── services.py         # Services d'import/export CSV
        └── views               # Organisation modulaire (blueprints)
            ├── __init__.py     # Application factory
            ├── cmd.py          # Commandes CLI
            ├── web_ui.py       # Interface web
            ├── api.py          # API REST
            ├── error_handlers.py # Gestion d'erreurs
            ├── templates       # Templates HTML
            └── static          # Assets statiques
```

## Fonctionnalités

### Interface CLI complète
```bash
$ pdm run flask --app archilog:create_app archilog
Usage: flask archilog [OPTIONS] COMMAND [ARGS]...

Commands:
  create      Créer une nouvelle entrée
  delete      Supprimer une entrée existante
  get         Récupérer une entrée par son ID
  get-all     Lister toutes les entrées (avec option CSV)
  import-csv  Importer des données depuis un fichier CSV
  init-db     Initialiser la base de données
  update      Mettre à jour une entrée existante
```

### Interface web intuitive
- Affichage de toutes les entrées financières
- Formulaires de création et modification
- Gestion des erreurs avec messages flash
- Design responsive

### API HTTP RESTful
| Verbe | Endpoint | Description | Authentification |
|-----------|----------|-------------|-----------------|
| GET | `/api/users/entries` | Récupérer toutes les entrées | Token requis |
| GET | `/api/users/entries/<id>` | Récupérer une entrée | Token requis |
| POST | `/api/users/entries` | Créer une entrée | Token admin |
| PUT | `/api/users/entries/<id>` | Mettre à jour une entrée | Token admin |
| DELETE | `/api/users/entries/<id>` | Supprimer une entrée | Token admin |

## Industrialisation

### Architecture modulaire
- **Blueprints Flask**: Organisation en modules réutilisables
- **Application Factory**: Création dynamique de l'application
- **Modèles/Services/Vues**: Séparation claire des responsabilités

### Configuration centralisée
```python
from dataclasses import dataclass
import os

@dataclass
class Config:
    DATABASE_URL: str
    DEBUG: bool
    SECRET_KEY: str

config = Config(
    DATABASE_URL=os.getenv("ARCHILOG_DATABASE_URL", "sqlite:///data.db"),
    DEBUG=os.getenv("ARCHILOG_DEBUG", "False") == "True",
    SECRET_KEY=os.getenv("ARCHILOG_FLASK_SECRET_KEY", "default_key")
)
```

### Sécurité et validation
- **Authentification**: Système basé sur les rôles (admin, user)
- **Validation WTForms**: Pour l'interface web
- **Validation Pydantic**: Pour l'API REST
- **Logging**: Traçabilité des actions et erreurs

## Installation et démarrage rapide

1. Installez PDM: `pip install pdm`
2. Installez les dépendances: `pdm install`
3. Configurez l'environnement avec `dev.env`:
   ```
   ARCHILOG_DATABASE_URL=sqlite:///data.db
   ARCHILOG_DEBUG=True
   ARCHILOG_FLASK_SECRET_KEY=your_secret_key_here
   ```
4. Initialisez la base de données: 
   ```
   pdm run flask --app archilog:create_app archilog init-db
   ```
5. Lancez l'application web:
   ```
   pdm run start
   ```

## Utilisation

### CLI
```bash
# Créer une entrée
pdm run flask --app archilog:create_app archilog create

# Exporter au format CSV
pdm run flask --app archilog:create_app archilog get-all --as-csv > export.csv
```

### Interface web
Accédez à http://localhost:5000 dans votre navigateur
- Utilisateur: `user` / Mot de passe: `user` (lecture seule)
- Utilisateur: `admin` / Mot de passe: `admin` (accès complet)

### API HTTP
```bash
# Récupérer toutes les entrées
curl -X GET http://localhost:5000/api/users/entries \
     -H "Authorization: Bearer admin_token"

# Documentation API
Ouvrir http://localhost:5000/apidoc/swagger
```

## Conclusion

Archilog illustre l'implémentation d'une application Python complète avec toutes les bonnes pratiques de développement moderne:
- Organisation modulaire avec blueprints
- Configuration centralisée
- Authentification et autorisation
- Validation des données
- Documentation automatique d'API
- Tests et gestion des erreurs