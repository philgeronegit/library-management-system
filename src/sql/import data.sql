INSERT INTO `utilisateurs` (`id_utilisateurs`, `nom`, `hash_mot_passe`, `email`, `telephone`, `statut`, `is_admin`) VALUES
(1, 'John Doe', '', 'john.doe@example.com', NULL, 'actif', False),
(2, 'Jane doe', '', 'jane.doe@example.com', NULL, 'actif', False),
(4, 'Bob Smith', '', 'bob.smith@example.com', NULL, 'inactif', False),
(5, 'Admin', '', 'admin@gmail.com', NULL, 'actif', True);

INSERT INTO `administrateurs` (`id_utilisateurs`) VALUES (5);

INSERT INTO `regles_prets` (`duree_maximale`, `penalite_retard`) VALUES
(30, 5);

INSERT INTO `auteurs` (`nom`, `prenom`) VALUES
('Tolkien', 'JRR'),
('Rowling', 'JK'),
('Martin', 'George R.R. '),
('Lee', 'Harper');

INSERT INTO `genres` (`nom`) VALUES
('Fantastique'),
('Horreur'),
('Policier'),
('Thriller'),
('Science-Fiction'),
('Roman');