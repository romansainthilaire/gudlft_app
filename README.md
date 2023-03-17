# GUDLFT APP

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

Ce projet a été réalisé dans le cadre de la formation OpenClassrooms *Développeur d'application - Python*.

→ Amélioration d'une application Python à l'aide du framework de tests **Pytest**.

## Présentation de l'application

L'application initiale à tester et débugger a été clonée depuis le dépôt suivant : https://github.com/OpenClassrooms-Student-Center/Python_Testing

L'application sert à la gestion d'inscriptions de clubs sportifs à des compétitions.

Les clubs gagnent des points via la mise en place de compétitions. Les clubs peuvent inscrire leurs membres à des compétitions en utilisant les points accumulés.

Exemple de parcours utilisateur :

- Le/La secrétaire du club se connecte à l'application.
- Le/La secrétaire identifie une compétition à venir, il/elle peut voir le nombre d'inscriptions disponibles et peut alors utiliser les points du club pour inscrire des membres à la compétition sélectionnée.
- Le/La secrétaire peut également consulter la liste des points des autres clubs.

A noter qu'il n'est pas possible d'inscrire plus de 12 membres d'un club à une compétition donnée.

## Installation
- créer un environnement virtuel : python -m venv [nom]
- activer l'environnement virtuel : [nom]\Scripts\activate
- installer les packages : pip install -r requirements.txt
- installer playwright : playwright install

## Lancement de l'application
- lancer le serveur de développement : flask run
- se rendre à l'adresse : http://127.0.0.1:5000/

## Exécution des tests unitaires
- exécuter les tests unitaires : pytest tests/unit_tests/test_server.py -v

## Exécution des tests fonctionnels
- lancer le serveur de développement : flask run
- exécuter les tests fonctionnels : pytest tests/functional_tests/test_server.py -v

## Exécution des tests de performance
- lancer le serveur de développement : flask run
- lancer locust : locust -f tests/performance_tests/test_server.py
- accéder à l'interface web locust : http://localhost:8089/

<ins>Note :</ins><br>
L'adresse du champ "Host" à renseigner est celle du serveur de développement (<span>http</span>://127.0.0.1:5000/). Les autres champs correspondent au nombre total d'utilisateurs à simuler et au nombre d'utilisateurs créés par seconde.

## Génération du rapport de couverture de tests
- lancer le serveur de développement : flask run
- générer le rapport html : pytest --cov=. --cov-report html

→ Un dossier "htmlcov" est créé à la racine du projet.

## Conventions de nommage

L'ajout de tests concernant une fonctionnalité de l'application, un bug ou une amélioration fait systématiquement l'objet de création d'une branche.

Le nom de la branche suit le format : **<feature/bug/improvement>/nom-descriptif**
