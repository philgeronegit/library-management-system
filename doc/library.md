# Description du Projet

Notre projet vise à développer une solution moderne et intuitive de gestion de bibliothèque qui
répond aux besoins tant des administrateurs que des utilisateurs finaux. Cette plateforme
numérique permettra d'optimiser la gestion des ressources bibliothécaires tout en offrant une
expérience utilisateur enrichie.
Fonctionnalités principales :
- Gestion des livres
- Gestion des utilisateurs
- Gestion des emprunts
- Gestion des retards
Spécifications Techniques
- Langage de programmation : Python
- SGBD : MySQL
- Interface graphique : PyQt pour une interface utilisateur ergonomique
- Tests : Tests unitaires avec Pytest
- Design pattern conseillé : MVC

# User stories
Les *user stories* suivantes définissent les exigences fonctionnelles du projet du point de vue
de l’administrateur et de l’utilisateur final. Elles couvrent les scénarios d’utilisation typiques
dans une application de gestion de bibliothèque.

## Administrateur
En tant qu’administrateur, je veux pouvoir :
1) ajouter de nouveaux livres à la bibliothèque afin d’enrichir la collection.
2) modifier les informations d’un livre existant (titre, auteur, genre, date de publication)
pour tenir à jour la collection.
3) supprimer un livre qui n’est plus disponible ou pertinent afin de maintenir une base de
données à jour.
4) consulter la liste complète des livres empruntés pour mieux gérer l’inventaire.
5) ajouter, modifier ou supprimer les informations des utilisateurs (nom, contact, statut)
pour une gestion efficace des membres.
6) superviser les emprunts et les retours de livres
7) consulter les retours en retard
8) contacter un utilisateur pour un retard.
9) consulter l’historique d’emprunts d’un utilisateur en particulier pour suivre son
comportement de prêt.

## Utilisateur
En tant qu’utilisateur :
1) rechercher un livre par titre, auteur ou catégorie pour le trouver rapidement dans la
collection.
2) consulter la disponibilité d’un livre pour savoir s’il est actuellement emprunté ou
disponible.
3) emprunter un livre en quelques clics à travers une interface intuitive.
4) consulter la liste des livres que j’ai empruntés ainsi que leurs dates de retour pour
mieux gérer mes emprunts.
5) prolonger la durée d’emprunt si le livre n’est pas réservé par un autre membre afin
d’éviter des pénalités.
6) réserver un livre actuellement emprunté par un autre utilisateur pour être notifié dès
qu’il sera disponible.
7) recevoir des rappels lorsque la date de retour d’un livre approche afin d’éviter des
retards.
8) consulter l’historique de mes emprunts passés pour voir les livres que j’ai déjà
empruntés.

## Règles métiers
- un emprunt ne peut durer que 3 semaines soit 21 jours.
- un emprunt peut être rallongé d'une semaine maximum sauf s'il est réservé.
- Un utilisateur peut réserver qu'un seul livre à la fois.
- lorsque un utilisateur n'a pas rendu un ou plusieurs livres, il est contacté par un
administrateur.
- Lorsque les retards sont trop nombreux, un administrateur peut choisir de bloquer un
utilisateur.

## Livrables
1) Diagramme UML : Use Case, Diagramme de classe, Diagramme d'interactions
2) MCD et le script SQL
3) Maquette Wireframe :
Un wireframe détaillant l’interface graphique utilisateur de l’application, montrant les
principales vues et fonctionnalités.
4) Diagramme explicatif sur l’architecture logicielle
Ce diagramme décompose l’architecture logicielle en couches expliquant le rôle de
chaque couche et la manière dont elles interagissent entre elles.
5) Lien github complété par un projet pour la gestion des tâches