# Présentation du Projet

Archilog est un projet éducatif complet qui combine plusieurs technologies modernes pour créer une application Python modulaire et évolutive. Elle offre une solution intégrée pour la gestion de données financières avec des interfaces en ligne de commande (CLI) et web.

## Vue d'ensemble

L'objectif principal est de fournir une application polyvalente répondant aux besoins suivants :

- **Interface en ligne de commande (CLI) :**  
  Utilisation de [Click](https://click.palletsprojects.com) pour créer des commandes interactives simples et efficaces. L'utilisateur peut :
  - Créer, modifier et supprimer des entrées financières
  - Exporter et importer des données au format CSV
  - Récupérer des entrées par identifiant unique

- **Gestion des données :**  
  Stockage et manipulation des données à l'aide de SQLite, en utilisant [SQLAlchemy Core](https://docs.sqlalchemy.org) pour interagir directement avec la base de données. Points clés :
  - Modèle de données flexible (entrées avec nom, montant, catégorie)
  - Validation syntaxique et sémantique des données
  - Gestion des erreurs et logging centralisé

- **Interface web :**  
  Création d'une application web à l'aide de [Flask](https://flask.palletsprojects.com) avec :
  - Templates dynamiques via Jinja2
  - Formulaires validés avec WTForms
  - Authentification et contrôle d'accès basé sur les rôles (RBAC)
  - Gestion des erreurs personnalisée

## Technologies Principales

- **SQLAlchemy Core** : Interaction bas niveau avec la base de données SQLite
- **Flask** : Framework web léger et modulaire
- **Jinja2** : Moteur de templates pour générer du HTML dynamique
- **WTForms** : Validation robuste des formulaires
- **Flask-HTTPAuth** : Authentification et gestion des accès

## Architecture et Industrialisation

### Modularité

- Architecture basée sur des Blueprints Flask
- Application factory pour une configuration dynamique
- Séparation claire des composants (modèles, vues, services)

### Configuration

- Gestion centralisée avec python-dotenv
- Support de configurations multi-environnements (dev, test, prod)
- Variables d'environnement avec préfixe pour plus de sécurité

### Validation et Sécurité

- Validation syntaxique et sémantique des données
- Logging détaillé des actions et erreurs
- Authentification avec gestion des rôles (admin, user)
- Sécurisation des mots de passe avec hashage

## Fonctionnalités Clés

- Gestion complète d'entrées financières
- Interface CLI riche et interactive
- Interface web intuitive
- Exportation/Importation CSV
- Authentification et contrôle d'accès
- Validation avancée des données
- Traçabilité via logging

## Conclusion

Archilog démontre comment combiner efficacement une interface CLI, une gestion de données robuste et une interface web sécurisée pour créer une application Python modulaire et évolutive.