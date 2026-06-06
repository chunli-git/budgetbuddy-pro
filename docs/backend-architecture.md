# BudgetBuddy Pro — Backend Architecture

## 1. Objectif du backend

Le backend de BudgetBuddy Pro est une API REST construite avec FastAPI.

Son rôle est de gérer toute la logique métier de l’application :

- création de comptes utilisateurs
- authentification sécurisée avec JWT
- gestion des transactions
- gestion des budgets
- gestion des objectifs d’épargne
- gestion des transactions récurrentes
- calculs du dashboard
- alertes intelligentes
- export CSV
- communication avec la base de données PostgreSQL

Le frontend React communiquera avec ce backend grâce à des requêtes HTTP.

---

## 2. Technologies utilisées

Le backend utilise :

- FastAPI pour créer l’API
- PostgreSQL pour stocker les données
- SQLAlchemy comme ORM
- Alembic pour les migrations de base de données
- Pydantic pour valider les données envoyées par l’utilisateur
- JWT pour l’authentification
- bcrypt/passlib pour sécuriser les mots de passe
- Docker pour lancer PostgreSQL facilement
- pytest pour les tests automatiques
- GitHub Actions pour lancer les tests automatiquement à chaque push

---

## 3. Organisation du code

Le dossier backend est organisé comme ceci :

- app/main.py : point d’entrée de l’application FastAPI
- app/database.py : connexion à PostgreSQL
- app/models/ : modèles SQLAlchemy, donc les tables de la base de données
- app/schemas/ : schémas Pydantic, donc la validation des données
- app/routers/ : routes API
- app/core/security.py : hash des mots de passe et création des tokens JWT
- app/core/dependencies.py : récupération de l’utilisateur connecté
- alembic/ : migrations de base de données
- tests/ : tests automatiques
- requirements.txt : dépendances Python
- .env.example : exemple des variables d’environnement nécessaires

---

## 4. Fonctionnement général

Quand un utilisateur utilise l’application :

1. Le frontend envoie une requête HTTP au backend.
2. FastAPI reçoit la requête.
3. Pydantic vérifie si les données sont valides.
4. La route appelle SQLAlchemy pour lire ou modifier PostgreSQL.
5. Le backend retourne une réponse JSON au frontend.

Exemple :

L’utilisateur ajoute une transaction.

Le frontend envoie :

POST /transactions/

Le backend vérifie :

- le montant est positif
- la description n’est pas vide
- la catégorie n’est pas vide
- le type est income ou expense
- l’utilisateur est connecté

Ensuite le backend sauvegarde la transaction dans PostgreSQL.

---

## 5. Authentification

L’authentification fonctionne avec JWT.

Lorsqu’un utilisateur se connecte avec son email et son mot de passe :

1. Le backend vérifie que l’email existe.
2. Le backend compare le mot de passe envoyé avec le mot de passe hashé.
3. Si tout est correct, le backend génère un token JWT.
4. Le frontend garde ce token.
5. Pour les routes protégées, le frontend renvoie ce token au backend.

Les routes protégées utilisent la fonction get_current_user.

Cette fonction permet de savoir quel utilisateur est connecté et empêche un utilisateur d’accéder aux données d’un autre utilisateur.

---

## 6. Base de données

La base de données utilisée est PostgreSQL.

Les principales tables sont :

- users
- transactions
- budgets
- savings_goals
- recurring_transactions

Chaque transaction, budget, objectif d’épargne et transaction récurrente est relié à un utilisateur grâce à user_id.

Cela permet à chaque utilisateur d’avoir uniquement ses propres données.

---

## 7. Migrations Alembic

Alembic permet de gérer l’évolution de la base de données.

À chaque fois qu’un nouveau modèle est ajouté ou modifié, une migration est créée.

Cela permet de garder un historique propre des changements de la base de données.

Exemples de migrations :

- création de la table users
- création de la table transactions
- création de la table budgets
- création de la table savings_goals
- création de la table recurring_transactions

---

## 8. Validation des données

Les validations sont faites avec Pydantic.

Exemples de règles :

- les montants doivent être positifs
- les noms ne doivent pas être vides
- transaction_type doit être income ou expense
- frequency doit être daily, weekly ou monthly
- les mots de passe doivent respecter une longueur valide

Ces validations empêchent l’utilisateur d’envoyer des données incorrectes à l’API.

---

## 9. Dashboard

Le dashboard regroupe plusieurs calculs importants :

- total des revenus
- total des dépenses
- solde
- dépenses par catégorie
- résumé mensuel
- statistiques globales
- transactions récentes
- score de santé budgétaire
- alertes intelligentes

Ces données seront affichées dans le frontend React sous forme de cartes, tableaux et graphiques.

---

## 10. Tests automatiques

Le backend contient des tests avec pytest.

Les tests vérifient notamment :

- que la route principale fonctionne
- que les transactions invalides sont refusées
- que les budgets invalides sont refusés
- que les objectifs d’épargne invalides sont refusés
- que les transactions récurrentes invalides sont refusées

Ces tests rendent le projet plus fiable et plus professionnel.

---

## 11. GitHub Actions

GitHub Actions lance automatiquement les tests backend à chaque push sur GitHub.

Cela permet de vérifier que le backend fonctionne encore après chaque modification.

Si un test échoue, GitHub affiche une erreur dans l’onglet Actions.

---

## 12. Conclusion

Le backend de BudgetBuddy Pro est construit comme une vraie API professionnelle.

Il contient :

- une architecture claire
- une base PostgreSQL
- une authentification JWT
- des routes protégées
- des validations propres
- des migrations
- des tests automatiques
- une CI GitHub Actions
- une documentation technique

Ce backend est prêt à être connecté à un frontend React.