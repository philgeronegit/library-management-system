# Plan de Tests pour l'Application de Gestion de Bibliothèque

## 1. Objectif du Plan de Test
Ce plan de test vise à vérifier le bon fonctionnement de l'application de gestion de bibliothèque, en s'assurant que toutes les fonctionnalités clés répondent aux exigences définies dans les user stories et aux règles métier. Les tests couvriront la création, modification, suppression, consultation et filtrage des données, ainsi que la validation des règles métier, la gestion des erreurs et la sécurité de base.

## 2. Périmètre
Les tests fonctionnels porteront sur :
- **Module de Gestion des Livres** : Ajout, modification, suppression et consultation des livres.
- **Module de Gestion des Utilisateurs** : Ajout, modification, suppression et consultation des utilisateurs.
- **Module de Gestion des Emprunts** : Emprunt, retour, prolongation, réservation, rappels et historique.
- **Module de Consultation et Filtrage** : Recherche par titre, auteur ou catégorie ; vérification de disponibilité.
- **Sécurité et Cohérence** : Accès non autorisé, injection SQL, validation des données incohérentes.

Les tests non couverts incluent les tests de performance, de charge ou d'interface utilisateur avancée (au-delà des fonctionnalités de base).

## 3. Environnement de Test
- **Version de l'application** : 1.0
- **Système d'exploitation** : Windows 10 (ou compatible)
- **Langage de programmation** : Python 3.10+
- **Base de données** : MySQL
- **Interface graphique** : PyQt
- **Comptes de test** : Administrateur (accès complet) et utilisateur standard (accès limité)
- **Outils** : Pytest pour les tests unitaires automatisés ; tests manuels pour l'interface utilisateur

## 4. Cas de Test

### 4.1 Gestion des Livres (Administrateur)
| ID | Préconditions | Action | Résultat Attendu |
|----|---------------|--------|------------------|
| CT-LIV-01 | Administrateur connecté | Ajouter un nouveau livre (titre, auteur, genre, date de publication) | Le livre est ajouté à la base de données et apparaît dans la liste des livres. |
| CT-LIV-02 | Livre existant dans la base | Modifier les informations d'un livre (titre, auteur, genre, date) | Les modifications sont sauvegardées et visibles dans la consultation. |
| CT-LIV-03 | Livre existant sans emprunt en cours | Supprimer un livre | Le livre est supprimé de la base de données. |
| CT-LIV-04 | Administrateur connecté | Consulter la liste complète des livres empruntés | Liste affichée avec détails (titre, emprunteur, date de retour). |
| CT-LIV-05 | Livre avec emprunt en cours | Tenter de supprimer un livre emprunté | Message d'erreur : "Impossible de supprimer un livre emprunté". |

### 4.2 Gestion des Utilisateurs (Administrateur)
| ID | Préconditions | Action | Résultat Attendu |
|----|---------------|--------|------------------|
| CT-USER-01 | Administrateur connecté | Ajouter un nouvel utilisateur (nom, contact, statut) | L'utilisateur est ajouté et apparaît dans la liste des utilisateurs. |
| CT-USER-02 | Utilisateur existant | Modifier les informations d'un utilisateur | Modifications sauvegardées et visibles. |
| CT-USER-03 | Utilisateur sans emprunt en cours | Supprimer un utilisateur | L'utilisateur est supprimé de la base. |
| CT-USER-04 | Administrateur connecté | Consulter l'historique d'emprunts d'un utilisateur | Historique affiché (livres empruntés, dates). |
| CT-USER-05 | Utilisateur avec retards nombreux | Bloquer un utilisateur | Statut de l'utilisateur mis à jour à "bloqué" ; emprunts interdits. |

### 4.3 Gestion des Emprunts (Administrateur et Utilisateur)
| ID | Préconditions | Action | Résultat Attendu |
|----|---------------|--------|------------------|
| CT-EMP-01 | Utilisateur connecté, livre disponible | Emprunter un livre | Emprunt enregistré pour 21 jours ; livre marqué comme indisponible. |
| CT-EMP-02 | Livre emprunté par l'utilisateur | Retourner un livre | Emprunt clôturé ; livre disponible ; historique mis à jour. |
| CT-EMP-03 | Emprunt en cours, pas réservé, moins de 7 jours restants | Prolonger l'emprunt d'une semaine | Durée étendue à 28 jours maximum. |
| CT-EMP-04 | Emprunt réservé par un autre utilisateur | Tenter de prolonger | Message d'erreur : "Prolongation impossible, livre réservé". |
| CT-EMP-05 | Utilisateur sans réservation active | Réserver un livre emprunté | Réservation enregistrée ; notification à préparer pour disponibilité. |
| CT-EMP-06 | Utilisateur avec une réservation active | Tenter de réserver un autre livre | Message d'erreur : "Une seule réservation autorisée à la fois". |
| CT-EMP-07 | Administrateur connecté | Consulter les retours en retard | Liste des emprunts en retard affichée. |
| CT-EMP-08 | Utilisateur en retard | Contacter l'utilisateur pour retard | Fonction de contact activée (e-mail ou notification simulée). |
| CT-EMP-09 | Utilisateur connecté | Consulter ses emprunts actifs | Liste affichée avec dates de retour. |
| CT-EMP-10 | Utilisateur connecté | Recevoir un rappel pour date de retour proche | Notification envoyée 3 jours avant échéance. |

### 4.4 Recherche et Consultation (Utilisateur)
| ID | Préconditions | Action | Résultat Attendu |
|----|---------------|--------|------------------|
| CT-SEARCH-01 | Utilisateur connecté | Rechercher un livre par titre | Résultats filtrés affichés. |
| CT-SEARCH-02 | Utilisateur connecté | Rechercher un livre par auteur | Résultats filtrés affichés. |
| CT-SEARCH-03 | Utilisateur connecté | Rechercher un livre par catégorie | Résultats filtrés affichés. |
| CT-SEARCH-04 | Utilisateur connecté | Vérifier la disponibilité d'un livre | Statut "disponible" ou "emprunté" affiché. |
| CT-SEARCH-05 | Utilisateur connecté | Consulter l'historique de ses emprunts passés | Liste des emprunts clôturés affichée. |

### 4.5 Sécurité et Cohérence
| ID | Préconditions | Action | Résultat Attendu |
|----|---------------|--------|------------------|
| CT-SEC-01 | Aucun utilisateur connecté | Tenter d'accéder à une fonctionnalité admin | Message d'erreur : "Accès refusé". |
| CT-SEC-02 | Formulaire de recherche ouvert | Saisir une chaîne SQL malveillante | Aucune donnée sensible exposée ; entrée gérée sans erreur. |
| CT-SEC-03 | Base de données valide | Créer un emprunt avec date de retour antérieure | Message d'erreur : "Dates incohérentes". |
| CT-SEC-04 | Utilisateur bloqué | Tenter d'emprunter un livre | Message d'erreur : "Utilisateur bloqué". |

## 5. Gestion des Anomalies
Toute anomalie détectée sera consignée avec :
- ID du test
- Description du problème
- Étapes pour reproduire
- Sévérité (faible, moyenne, élevée)
- Statut (nouveau, en cours, résolu)

Les anomalies peuvent être enregistrées comme des issues dans le dépôt GitHub pour un suivi collaboratif.

## 6. Exécution des Tests
- **Tests manuels** : Pour l'interface utilisateur et les scénarios complexes.
- **Tests automatisés** : Avec Pytest pour les tests unitaires sur les contrôleurs, managers et repositories.
- **Fréquence** : Tests complets avant chaque release ; tests de régression après corrections.

Ce plan couvre toutes les fonctionnalités principales et règles métier. Il peut être ajusté en fonction des évolutions du code.