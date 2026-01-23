-- Script de création de la base de données bibliotheque
-- Ce script crée toutes les tables nécessaires pour le système de gestion de bibliothèque

CREATE DATABASE bibliotheque;

USE bibliotheque;

-- Création de la table utilisateurs : stocke les informations des utilisateurs du système
CREATE TABLE utilisateurs(
   id_utilisateurs INT AUTO_INCREMENT,
   nom VARCHAR(255)  NOT NULL,
   hash_mot_passe VARCHAR(255)  NOT NULL,
   email VARCHAR(55)  NOT NULL,
   telephone VARCHAR(15) ,
   date_naissance DATE NOT NULL,
   statut enum('actif', 'inactif', 'en-attente') NOT NULL,
   is_admin BOOLEAN NOT NULL default False,
   PRIMARY KEY(id_utilisateurs),
   UNIQUE(email),
   UNIQUE(telephone)
);


-- Création de la table regles_prets : définit les règles de prêt (durée maximale, pénalité)
CREATE TABLE regles_prets(
   id_regles_prets INT AUTO_INCREMENT,
   duree_maximale SMALLINT NOT NULL,
   penalite_retard SMALLINT NOT NULL,
   date_fin_validite DATE,
   PRIMARY KEY(id_regles_prets)
);

-- Création de la table genres : liste des genres littéraires disponibles
CREATE TABLE genres(
   id_genres INT AUTO_INCREMENT,
   nom VARCHAR(50) ,
   PRIMARY KEY(id_genres),
   UNIQUE(nom)
);

-- Création de la table auteurs : informations sur les auteurs des livres
CREATE TABLE auteurs(
   id_auteurs INT AUTO_INCREMENT,
   nom VARCHAR(50)  NOT NULL,
   prenom VARCHAR(50) ,
   PRIMARY KEY(id_auteurs)
);

-- Création de la table collections : groupes de livres (séries, collections éditoriales)
CREATE TABLE collections(
   id_collections INT AUTO_INCREMENT,
   nom VARCHAR(50)  NOT NULL,
   PRIMARY KEY(id_collections),
   UNIQUE(nom)
);

-- Création de la table administrateurs : utilisateurs ayant des droits d'administration
CREATE TABLE administrateurs(
   id_utilisateurs INT,
   PRIMARY KEY(id_utilisateurs),
   FOREIGN KEY(id_utilisateurs) REFERENCES utilisateurs(id_utilisateurs)
);

-- Création de la table livres : informations détaillées sur chaque livre
CREATE TABLE livres(
   id_livres INT AUTO_INCREMENT,
   titre VARCHAR(255)  NOT NULL,
   date_publication DATE NOT NULL,
   date_creation DATETIME NOT NULL,
   date_suppression DATETIME,
   cree_par INT,
   supprime_par INT,
   id_collections INT,
   id_genres INT NOT NULL,
   PRIMARY KEY(id_livres),
   FOREIGN KEY(cree_par) REFERENCES administrateurs(id_utilisateurs),
   FOREIGN KEY(supprime_par) REFERENCES administrateurs(id_utilisateurs),
   FOREIGN KEY(id_collections) REFERENCES collections(id_collections),
   FOREIGN KEY(id_genres) REFERENCES genres(id_genres)
);

-- Création de la table emprunts : enregistrements des emprunts de livres
CREATE TABLE emprunts(
   id_emprunts INT AUTO_INCREMENT,
   date_emprunt DATE NOT NULL,
   date_retour DATE,
   id_regles_prets INT NOT NULL,
   id_livres INT NOT NULL,
   id_utilisateurs INT NOT NULL,
   PRIMARY KEY(id_emprunts),
   FOREIGN KEY(id_regles_prets) REFERENCES regles_prets(id_regles_prets),
   FOREIGN KEY(id_livres) REFERENCES livres(id_livres),
   FOREIGN KEY(id_utilisateurs) REFERENCES utilisateurs(id_utilisateurs)
);

-- Création de la table reservations : réservations de livres par les utilisateurs
CREATE TABLE reservations(
   id_reservations INT AUTO_INCREMENT,
   date_reservation DATE,
   id_livres INT NOT NULL,
   id_utilisateurs INT NOT NULL,
   PRIMARY KEY(id_reservations),
   UNIQUE(id_utilisateurs),
   FOREIGN KEY(id_livres) REFERENCES livres(id_livres),
   FOREIGN KEY(id_utilisateurs) REFERENCES utilisateurs(id_utilisateurs)
);

-- Création de la table notifications : messages système pour les utilisateurs
CREATE TABLE notifications(
   id_notifications INT AUTO_INCREMENT,
   type enum('info', 'alerte') NOT NULL,
   contenu VARCHAR(255)  NOT NULL,
   date_notification DATETIME NOT NULL,
   date_lecture DATETIME,
   id_emprunts INT,
   id_reservations INT,
   id_utilisateurs INT NOT NULL,
   PRIMARY KEY(id_notifications),
   FOREIGN KEY(id_emprunts) REFERENCES emprunts(id_emprunts),
   FOREIGN KEY(id_reservations) REFERENCES reservations(id_reservations),
   FOREIGN KEY(id_utilisateurs) REFERENCES utilisateurs(id_utilisateurs)
);

-- Création de la table est_ecrit_par : relation many-to-many entre livres et auteurs
CREATE TABLE est_ecrit_par(
   id_livres INT,
   id_auteurs INT,
   PRIMARY KEY(id_livres, id_auteurs),
   FOREIGN KEY(id_livres) REFERENCES livres(id_livres),
   FOREIGN KEY(id_auteurs) REFERENCES auteurs(id_auteurs)
);

-- Création de la table modifie : historique des modifications apportées aux livres par les administrateurs
CREATE TABLE modifie(
   id_livres INT,
   id_utilisateurs INT,
   date_modification DATETIME,
   PRIMARY KEY(id_livres, id_utilisateurs),
   FOREIGN KEY(id_livres) REFERENCES livres(id_livres),
   FOREIGN KEY(id_utilisateurs) REFERENCES administrateurs(id_utilisateurs)
);