import uuid
import io
import click
from flask import Blueprint, jsonify, request

import archilog.models as models
import archilog.services as services

# Blueprint pour l'API et les commandes CLI
api = Blueprint("api", __name__, url_prefix="/api", cli_group="archilog")

# Routes API - facultatif, mais cela montre comment séparer les fonctionnalités
@api.route('/entries', methods=['GET'])
def get_entries():
    entries = models.get_all_entries()
    return jsonify([{
        'id': entry.id.hex,
        'name': entry.name,
        'amount': entry.amount,
        'category': entry.category
    } for entry in entries])

# Commandes CLI
@api.cli.command("init-db")
def init_db():
    models.init_db()
    click.echo("Base de données initialisée avec succès.")

@api.cli.command("create")
@click.option("-n", "--name", prompt="Name")
@click.option("-a", "--amount", type=float, prompt="Amount")
@click.option("-c", "--category", default=None)
def create(name: str, amount: float, category: str | None):
    models.create_entry(name, amount, category)
    click.echo(f"Entrée créée: {name}, {amount}, {category}")

@api.cli.command("get")
@click.option("--id", required=True, type=click.UUID)
def get(id: uuid.UUID):
    entry = models.get_entry(id)
    click.echo(entry)

@api.cli.command("get-all")
@click.option("--as-csv", is_flag=True, help="Output a CSV string.")
def get_all(as_csv: bool):
    if as_csv:
        click.echo(services.export_to_csv().getvalue())
    else:
        for entry in models.get_all_entries():
            click.echo(entry)

@api.cli.command("import-csv")
@click.argument("csv_file", type=click.File("r"))
def import_csv_cmd(csv_file):
    services.import_from_csv(csv_file)
    click.echo("Import CSV terminé.")

@api.cli.command("update")
@click.option("--id", type=click.UUID, required=True)
@click.option("-n", "--name", required=True)
@click.option("-a", "--amount", type=float, required=True)
@click.option("-c", "--category", default=None)
def update(id: uuid.UUID, name: str, amount: float, category: str | None):
    models.update_entry(id, name, amount, category)
    click.echo(f"Entrée mise à jour: {id}, {name}, {amount}, {category}")

@api.cli.command("delete")
@click.option("--id", required=True, type=click.UUID)
def delete(id: uuid.UUID):
    models.delete_entry(id)
    click.echo(f"Entrée avec ID {id} supprimée.")