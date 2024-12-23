import sqlalchemy

from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.utils.constants import (
    ALL_BOOKS,
    AVAILABLE_BOOKS,
    BORROWED_BOOKS,
    DELETED_BOOKS,
    LATE_BOOKS,
    SEARCH_BOOKS,
    USER_BOOKS,
)


class BookRepository:
    def __init__(self, database: Database):
        self.database = database

    def read_all(self, filter_type="all", filter_text=""):
        query = ""
        if filter_type == ALL_BOOKS:
            query = """
              SELECT
                l.id_livres AS ID,
                l.titre AS Titre,
                GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom)
                    SEPARATOR ', ') AS Auteurs,
                g.nom AS Genre,
                l.date_publication AS 'Date publication',
                e.date_emprunt AS 'Date emprunt',
                e.id_utilisateurs as 'Emprunté par',
                e.date_retour AS 'Date retour',
                l.date_creation AS 'Date création',
                l.cree_par AS 'Créé par',
                m.date_modification AS 'Date modification',
                u.id_utilisateurs AS 'Modifié par',
                l.date_suppression AS 'Date suppression',
                l.supprime_par AS 'Supprimé par',
                GROUP_CONCAT(a.id_auteurs
                    SEPARATOR ', ') AS 'ID auteurs',
                g.id_genres AS 'ID genre'
            FROM
                livres l
                    JOIN
                est_ecrit_par ep ON ep.id_livres = l.id_livres
                    JOIN
                auteurs a ON ep.id_auteurs = a.id_auteurs
                    JOIN
                genres g ON g.id_genres = l.id_genres
                    LEFT JOIN
                emprunts e ON l.id_livres = e.id_livres
                    LEFT JOIN
                modifie m ON m.id_livres = l.id_livres
                    LEFT JOIN
                utilisateurs u ON u.id_utilisateurs = m.id_utilisateurs
            WHERE l.date_suppression IS NULL
            GROUP BY l.id_livres;
          """
        elif filter_type == USER_BOOKS:
            query = f"""
              SELECT
                l.id_livres AS ID,
                l.titre AS Titre,
                GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom)
                    SEPARATOR ', ') AS Auteurs,
                g.nom AS Genre,
                l.date_publication AS 'Date publication',
                e.date_emprunt AS 'Date emprunt',
                e.id_utilisateurs as 'Emprunté par',
                e.date_retour AS 'Date retour',
                l.date_creation AS 'Date création',
                l.cree_par AS 'Créé par',
                m.date_modification AS 'Date modification',
                u.id_utilisateurs AS 'Modifié par',
                l.date_suppression AS 'Date suppression',
                l.supprime_par AS 'Supprimé par',
                GROUP_CONCAT(a.id_auteurs
                    SEPARATOR ', ') AS 'ID auteurs',
                g.id_genres AS 'ID genre'
            FROM
                livres l
                    JOIN
                est_ecrit_par ep ON ep.id_livres = l.id_livres
                    JOIN
                auteurs a ON ep.id_auteurs = a.id_auteurs
                    JOIN
                genres g ON g.id_genres = l.id_genres
                    LEFT JOIN
                emprunts e ON l.id_livres = e.id_livres
                    LEFT JOIN
                modifie m ON m.id_livres = l.id_livres
                    LEFT JOIN
                utilisateurs u ON u.id_utilisateurs = m.id_utilisateurs
            WHERE l.date_suppression IS NULL AND
              e.id_utilisateurs = {filter_text}
            GROUP BY l.id_livres;
          """
        elif filter_type == DELETED_BOOKS:
            query = """
              SELECT
                l.id_livres AS ID,
                l.titre AS Titre,
                GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom)
                    SEPARATOR ', ') AS Auteurs,
                g.nom AS Genre,
                l.date_publication AS 'Date publication',
                e.date_emprunt AS 'Date emprunt',
                e.id_utilisateurs as 'Emprunté par',
                e.date_retour AS 'Date retour',
                l.date_creation AS 'Date création',
                l.cree_par AS 'Créé par',
                m.date_modification AS 'Date modification',
                u.id_utilisateurs AS 'Modifié par',
                l.date_suppression AS 'Date suppression',
                l.supprime_par AS 'Supprimé par',
                GROUP_CONCAT(a.id_auteurs
                    SEPARATOR ', ') AS 'ID auteurs',
                g.id_genres AS 'ID genre'
            FROM
                livres l
                    JOIN
                est_ecrit_par ep ON ep.id_livres = l.id_livres
                    JOIN
                auteurs a ON ep.id_auteurs = a.id_auteurs
                    JOIN
                genres g ON g.id_genres = l.id_genres
                    LEFT JOIN
                emprunts e ON l.id_livres = e.id_livres
                    LEFT JOIN
                modifie m ON m.id_livres = l.id_livres
                    LEFT JOIN
                utilisateurs u ON u.id_utilisateurs = m.id_utilisateurs
            WHERE l.date_suppression IS NOT NULL
            GROUP BY l.id_livres;
          """
        elif filter_type == SEARCH_BOOKS:
            query = f"""
              SELECT * FROM
              (SELECT
                  l.id_livres AS ID,
                  l.titre AS Titre,
                  GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom) SEPARATOR ', ') AS Auteurs,
                  g.nom AS Genre,
                  l.date_publication AS 'Date publication',
                  e.date_emprunt AS 'Date emprunt',
                  e.id_utilisateurs as 'Emprunté par',
                  e.date_retour AS 'Date retour',
                  u.nom AS Utilisateur,
                  l.date_suppression AS 'Date suppression',
                  GROUP_CONCAT(a.id_auteurs SEPARATOR ', ') AS 'ID auteurs',
                  g.id_genres AS 'ID genre'
              FROM
                  livres l
              JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
		          JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
              JOIN genres g ON g.id_genres = l.id_genres
              LEFT JOIN emprunts e ON l.id_livres = e.id_livres
              LEFT JOIN utilisateurs u ON u.id_utilisateurs = e.id_utilisateurs
              GROUP BY l.id_livres) AS livres
              WHERE titre LIKE '%{filter_text}%' OR auteurs LIKE '%{filter_text}%' OR genre LIKE '%{filter_text}%'
            """
        elif filter_type == AVAILABLE_BOOKS:
            query = """
              SELECT
                  l.id_livres AS ID,
                  l.titre AS Titre,
                  GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom) SEPARATOR ', ') AS Auteurs,
                  g.nom AS Genre,
                  l.date_publication AS 'Date publication',
                  e.date_emprunt AS 'Date emprunt',
                  e.date_retour AS 'Date retour',
                  u.nom AS Utilisateur,
                  GROUP_CONCAT(a.id_auteurs SEPARATOR ', ') AS 'ID auteurs',
                  g.id_genres AS 'ID genre',
                  l.date_suppression AS 'Date suppression'
              FROM
                  livres l
              JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
			        JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
              JOIN genres g ON g.id_genres = l.id_genres
              LEFT JOIN emprunts e ON l.id_livres = e.id_livres
              LEFT JOIN utilisateurs u ON u.id_utilisateurs = e.id_utilisateurs
              WHERE (e.date_emprunt IS NULL OR e.date_retour IS NOT NULL)
                AND l.date_suppression IS NULL
              GROUP BY l.id_livres
            """
        elif filter_type == BORROWED_BOOKS:
            where_clause = ""
            if filter_text != "":
                where_clause = f" AND e.id_utilisateurs = {filter_text}"
            query = f"""
              SELECT
                  l.id_livres AS ID,
                  l.titre AS Titre,
                  GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom) SEPARATOR ', ') AS Auteurs,
                  g.nom AS Genre,
                  l.date_publication AS 'Date publication',
                  e.date_emprunt AS 'Date emprunt',
                  e.id_utilisateurs as 'Emprunté par',
                  e.date_retour AS 'Date retour',
                  u.nom AS Utilisateur,
                  l.date_suppression AS 'Date suppression',
                  GROUP_CONCAT(a.id_auteurs SEPARATOR ', ') AS 'ID auteurs',
                  g.id_genres AS 'ID genre'
              FROM
                  livres l
              JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
			        JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
              JOIN genres g ON g.id_genres = l.id_genres
              LEFT JOIN emprunts e ON l.id_livres = e.id_livres
              LEFT JOIN utilisateurs u ON u.id_utilisateurs = e.id_utilisateurs
              WHERE e.date_emprunt IS NOT NULL AND e.date_retour IS NULL
                AND l.date_suppression IS NULL {where_clause}
              GROUP BY l.id_livres;
            """
        elif filter_type == LATE_BOOKS:
            query = """
              SELECT
                  *
              FROM
                  (SELECT
                      l.id_livres AS ID,
                          l.titre AS Titre,
                          GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom) SEPARATOR ', ') AS Auteurs,
                          g.nom AS Genre,
                          l.date_publication AS 'Date publication',
                          e.date_emprunt AS 'Date emprunt',
                          e.id_utilisateurs as 'Emprunté par',
                          e.date_retour AS 'Date retour',
                          u.nom AS Utilisateur,
                          l.date_suppression AS 'Date suppression',
                          rp.duree_maximale_emprunt AS Max,
                          CURDATE() AS Now,
                          DATE_ADD(e.date_emprunt, INTERVAL rp.duree_maximale_emprunt DAY) AS Limite,
                          CASE
                              WHEN
                                  e.date_emprunt IS NULL
                                      AND e.date_retour IS NULL
                              THEN
                                  'Libre'
                              WHEN
                                  e.date_emprunt IS NOT NULL
                                      AND e.date_retour IS NOT NULL
                              THEN
                                  'Rendu'
                              WHEN
                                  e.date_emprunt IS NOT NULL
                                      AND e.date_retour IS NULL
                                      AND DATE_ADD(e.date_emprunt, INTERVAL rp.duree_maximale_emprunt DAY) < CURDATE()
                              THEN
                                  'En retard'
                              ELSE 'En cours'
                          END AS 'Status',
                          GROUP_CONCAT(a.id_auteurs SEPARATOR ', ') AS 'ID auteurs',
                          g.id_genres AS 'ID genre'
                  FROM
                      livres l
                  JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
		              JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
                  JOIN genres g ON g.id_genres = l.id_genres
                  LEFT JOIN emprunts e ON l.id_livres = e.id_livres
                  LEFT JOIN utilisateurs u ON u.id_utilisateurs = e.id_utilisateurs
                  LEFT JOIN regles_prets rp ON 1 = 1
                  WHERE l.date_suppression IS NULL
                  GROUP BY l.id_livres
              ) AS Livres
              WHERE Status = 'En retard';
            """

        return self.database.exec_query(query)

    def insert(self, book: Book, user_id: int):
        insert_book_query = f"""
          INSERT INTO livres
            (titre, date_publication, id_genres, date_creation, cree_par)
          VALUES
            ('{book.title}', '{book.publication_date}', {book.genre.id}, CURTIME(), '{user_id}')
        """
        try:
            engine = self.database.getEngine()
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(insert_book_query))
                book_id = result.lastrowid  # Get the auto-generated id_livres

                for auteur in book.authors:
                    insert_author_query = f"""
                    INSERT INTO est_ecrit_par
                      (id_auteurs, id_livres)
                    VALUES
                      ({auteur.id}, {book_id})
                    """
                    conn.execute(sqlalchemy.text(insert_author_query))

                conn.commit()
        except Exception as e:
            print("Erreur lors de l'insertion du livre et des auteurs {}".format(e))

    def modify(self, book: Book, user_id: int):
        modifie_livre_query = f"""
          INSERT INTO modifie (id_livres, id_utilisateurs, date_modification)
          VALUES ({book.id}, {user_id}, CURTIME())
          ON DUPLICATE KEY UPDATE date_modification = CURTIME();
        """
        delete_authors_query = f"""
          DELETE FROM est_ecrit_par
          WHERE id_livres = {book.id}
        """
        update_book_query = f"""
          UPDATE livres
          SET titre = '{book.title}', date_publication = '{book.publication_date}', id_genres = {book.genre.id}
          WHERE id_livres = {book.id}
        """
        queries = [modifie_livre_query, delete_authors_query, update_book_query]
        for auteur in book.authors:
            query = f"""
            INSERT INTO est_ecrit_par
              (id_auteurs, id_livres)
            VALUES
              ({auteur.id}, {book.id})
          """
            queries.append(query)

        self.database.exec_queries_with_commit(queries)

    def delete(self, book_id: int, user_id: int):
        delete_livre_query = f"""
          UPDATE livres
          SET date_suppression = CURTIME(),
              supprime_par = {user_id}
          WHERE id_livres = {book_id}
        """
        delete_emprunts_query = f"DELETE FROM emprunts WHERE id_livres = {book_id}"
        delete_reservations_query = (
            f"DELETE FROM reservations WHERE id_livres = {book_id}"
        )
        queries = [delete_livre_query, delete_emprunts_query, delete_reservations_query]
        self.database.exec_queries_with_commit(queries)

    def borrow_book(self, book_id, user_id):
        query = f"""
          INSERT INTO emprunts
            (date_emprunt, id_livres, id_utilisateurs)
          VALUES
            (CURDATE(), '{book_id}', {user_id})
        """
        self.database.exec_query_with_commit(query)

    def return_book(self, book_id, user_id):
        query = f"""
          UPDATE emprunts
          SET date_retour = CURDATE()
          WHERE id_livres = {book_id} AND id_utilisateurs = {user_id}
        """
        print("return query: ", query)
        self.database.exec_query_with_commit(query)
        query = f"""
          UPDATE emprunts
          SET date_retour = CURDATE()
          WHERE id_livres = {book_id} AND id_utilisateurs = {user_id}
        """
        print("return query: ", query)
        self.database.exec_query_with_commit(query)
