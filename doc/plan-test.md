1. Objectif du Plan de test
Ce plan de test a pour objectif de vérifier le bon fonctionnement de l’application de gestion de
livres, notamment :
- la création, la modification et la suppression de livres et d’utilisateurs ;
- la consultation et le filtrage des informations ;
- la validation des règles métier et le traitement des erreurs.

2. Périmètre
Tests fonctionnels portant sur :
- le module de Gestion des Livres ;
- le module de Gestion des Utilisateurs ;
- le module de Gestion des Emprunts ;
- le module de Consultation et Filtrage ;
- la sécurité de base.

3. Environnement de test
- Version de l’application : 1.0
- Système d’exploitation : Windows 10
- Langage de programmation : Python 3.10
- Base de données : MySQL
- Compte administrateur et compte utilisateur standard

4. Cas de test

4.4 Sécurité & cohérence
ID Cas de test Préconditions Action Résultat attendu
CT-SEC-01 Accès non autorisé à une fonctionnalité restreinte Aucun utilisateur connecté Tenter d’accéder à une fonctionnalité réservée aux administrateurs Message d’erreur indiquant l’accès refusé
CT-SEC-02 Injection SQL Formulaire de recherche ouvert Saisir une chaîne malveillante dans le champ de recherche Aucune donnée sensible n’est exposée, et l’application gère correctement l’entrée
CT-SEC-03 Données incohérentes Base de données avec des données valides Tenter de créer un emprunt avec une date de retour antérieure à la date d’emprunt Message d’erreur indiquant que les dates sont incohérentes

5. Gestion des anomalies
Toute anomalie détectée doit être consignée avec les informations suivantes :
- ID du test ;
- description du problème ;
- étapes pour reproduire ;
- sévérité ;
- statut (nouveau, en cours, résolu).
Lorsqu’un test révèle une anomalie (résultat inattendu ou bug), elle peut être enregistrée comme une issue dans le dépôt GitHub du projet. Cela permet de garder une trace claire des problèmes, d’attribuer leur résolution à un membre de l’équipe et de suivre leur correction.
Le dépôt GitHub n’est pas seulement un lieu pour stocker le code, c’est aussi un outil de gestion de projet efficace pour organiser les tâches, les bugs et les améliorations.

6. Explications

6.1 Plan de test
Un plan de test est un document structuré qui décrit les tests à faire sur l’application entière ou un module pour vérifier que les exigences métier sont respectées.
Il peut inclure des tests manuels ou automatisés, mais il ne détaille pas le code.
Son objectif est de couvrir toutes les fonctionnalités importantes et vérifier les règles métier ( vérifier que l’utilisateur peut créer un projet et ajouter des notes, que l’application gère les
dates incohérentes, etc.)

6.2 Périmètre des tests
Le périmètre du test précise quelles fonctionnalités de l’application seront testées et lesquelles ne le seront pas.
Par exemple, nous allons tester la création, la modification et la suppression de livres, ainsi que la consultation et le filtrage des informations.

6.3 Type de test à retenir
- Tests fonctionnels : vérifier que le logiciel fait bien ce qu’il doit faire
- Tests d’intégration : vérifier que différents modules ou systèmes communiquent correctement entre eux.
- Tests de sécurité : s’assurer qu’il n’y a pas de faille (XSS, injections SQL, accès non autorisés, etc.).