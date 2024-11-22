from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.models.book import Book


class BookDAL:
    def __init__(self, database: Database):
        self.database = database

    def read_books(self, filter_type="all", filter_text=""):
        query = ""
        if filter_type == "all":
            query = """
            SELECT
              id_livres AS ID,
              titre AS Titre,
              CONCAT(auteurs.prenom, ' ', auteurs.nom) AS Auteur,
              genres.nom AS Genre,
              date_publication AS 'Date publication',
              auteurs.id_auteurs AS 'ID Auteur',
              genres.id_genres AS 'ID Genre'
            FROM livres
            JOIN auteurs ON auteurs.id_auteurs = livres.id_auteurs
            JOIN genres ON genres.id_genres = livres.id_genres;
          """
        elif filter_type == "search":
            query = f"""
              SELECT
                id_livres AS ID,
                titre AS Titre,
                CONCAT(auteurs.prenom, ' ', auteurs.nom) AS Auteur,
                genres.nom AS Genre,
                date_publication AS 'Date publication'
              FROM livres
              JOIN auteurs ON auteurs.id_auteurs = livres.id_auteurs
              JOIN genres ON genres.id_genres = livres.id_genres
              WHERE titre LIKE '%{filter_text}%';
            """
        elif filter_type == "available":
            query = """
              SELECT
                  livres.id_livres AS ID,
                  livres.titre AS Titre,
                  CONCAT(auteurs.prenom, ' ', auteurs.nom) AS Auteur,
                  genres.nom AS Genre,
                  livres.date_publication AS 'Date publication',
                  emprunts.date_emprunt AS 'Date emprunt',
                  emprunts.date_retour AS 'Date retour',
                  utilisateurs.nom AS Utilisateur
              FROM
                  livres
              JOIN auteurs ON auteurs.id_auteurs = livres.id_auteurs
              JOIN genres ON genres.id_genres = livres.id_genres
              LEFT JOIN emprunts ON livres.id_livres = emprunts.id_livres
              LEFT JOIN utilisateurs ON utilisateurs.id_utilisateurs = emprunts.id_utilisateurs
              WHERE emprunts.date_emprunt IS NULL;
            """
        elif filter_type == "borrowed":
            query = """
              SELECT
                  livres.id_livres AS ID,
                  livres.titre AS Titre,
                  CONCAT(auteurs.prenom, ' ', auteurs.nom) AS Auteur,
                  genres.nom AS Genre,
                  livres.date_publication AS 'Date publication',
                  emprunts.date_emprunt AS 'Date emprunt',
                  emprunts.date_retour AS 'Date retour',
                  utilisateurs.nom AS Utilisateur
              FROM
                  livres
              JOIN auteurs ON auteurs.id_auteurs = livres.id_auteurs
              JOIN genres ON genres.id_genres = livres.id_genres
              LEFT JOIN emprunts ON livres.id_livres = emprunts.id_livres
              LEFT JOIN utilisateurs ON utilisateurs.id_utilisateurs = emprunts.id_utilisateurs
              WHERE emprunts.date_emprunt IS NOT NULL;
            """
        elif filter_type == "late":
            query = """
              SELECT
                  *
              FROM
                  (SELECT
                      livres.id_livres AS ID,
                          livres.titre AS Titre,
                          CONCAT(auteurs.prenom, ' ', auteurs.nom) AS Auteur,
                          genres.nom AS Genre,
                          livres.date_publication AS 'Date publication',
                          emprunts.date_emprunt AS 'Date emprunt',
                          emprunts.date_retour AS 'Date retour',
                          utilisateurs.nom AS Utilisateur,
                          regles_prets.duree_maximale_emprunt AS Max,
                          CURDATE() AS Now,
                          DATE_ADD(emprunts.date_emprunt, INTERVAL regles_prets.duree_maximale_emprunt DAY) AS Limite,
                          CASE
                              WHEN
                                  emprunts.date_emprunt IS NULL
                                      AND emprunts.date_retour IS NULL
                              THEN
                                  'Libre'
                              WHEN
                                  emprunts.date_emprunt IS NOT NULL
                                      AND emprunts.date_retour IS NOT NULL
                              THEN
                                  'Rendu'
                              WHEN
                                  emprunts.date_emprunt IS NOT NULL
                                      AND emprunts.date_retour IS NULL
                                      AND DATE_ADD(emprunts.date_emprunt, INTERVAL regles_prets.duree_maximale_emprunt DAY) < CURDATE()
                              THEN
                                  'En retard'
                              ELSE 'En cours'
                          END AS 'Status'
                  FROM
                      livres
                  JOIN auteurs ON auteurs.id_auteurs = livres.id_auteurs
                  JOIN genres ON genres.id_genres = livres.id_genres
                  LEFT JOIN emprunts ON livres.id_livres = emprunts.id_livres
                  LEFT JOIN utilisateurs ON utilisateurs.id_utilisateurs = emprunts.id_utilisateurs
                  LEFT JOIN regles_prets ON 1 = 1) AS Livres
              WHERE
                  Status = 'En retard';
            """

        return self.database.exec_query(query)

    def insert_book(self, book: Book):
        query = f"""
          INSERT INTO livres
            (titre, date_publication, id_auteurs, id_genres)
          VALUES
            ('{book.titre}', '{book.date_publication}', {book.auteur.id}, {book.genre.id})
        """
        self.database.exec_query_with_commit(query)

    def modify_book(self, book: Book):
        query = f"""
          UPDATE livres
          SET titre = '{book.titre}', date_publication = '{book.date_publication}', id_auteurs = {book.auteur.id}, id_genres = {book.genre.id}
          WHERE id_livres = {book.id}
        """
        self.database.exec_query_with_commit(query)

    def delete_book(self, book_id: int):
        query = f"DELETE FROM livres WHERE id_livres = {book_id}"
        self.database.exec_query_with_commit(query)
