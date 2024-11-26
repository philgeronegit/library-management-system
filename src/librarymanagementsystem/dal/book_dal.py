from datetime import datetime

import sqlalchemy

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
                  l.id_livres AS ID,
                  l.titre AS Titre,
                  GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom) SEPARATOR ', ') AS Auteurs,
                  g.nom AS Genre,
                  l.date_publication AS 'Date publication',
                  e.date_emprunt AS 'Date emprunt',
                  e.date_retour AS 'Date retour',
                  GROUP_CONCAT(a.id_auteurs SEPARATOR ', ') AS 'ID auteurs',
                  g.id_genres AS 'ID genre'
              FROM
                  livres l
              JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
		          JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
              JOIN genres g ON g.id_genres = l.id_genres
              JOIN emprunts e ON l.id_livres = e.id_livres
              GROUP BY l.id_livres;
          """
        elif filter_type == "search":
            query = f"""
              SELECT * FROM
              (SELECT
                  l.id_livres AS ID,
                  l.titre AS Titre,
                  GROUP_CONCAT(CONCAT(a.prenom, ' ', a.nom) SEPARATOR ', ') AS Auteurs,
                  g.nom AS Genre,
                  l.date_publication AS 'Date publication',
                  e.date_emprunt AS 'Date emprunt',
                  e.date_retour AS 'Date retour',
                  u.nom AS Utilisateur,
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
        elif filter_type == "available":
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
                  g.id_genres AS 'ID genre'
              FROM
                  livres l
              JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
			        JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
              JOIN genres g ON g.id_genres = l.id_genres
              LEFT JOIN emprunts e ON l.id_livres = e.id_livres
              LEFT JOIN utilisateurs u ON u.id_utilisateurs = e.id_utilisateurs
              WHERE e.date_emprunt IS NULL OR e.date_retour IS NOT NULL
              GROUP BY l.id_livres
            """
        elif filter_type == "borrowed":
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
                  g.id_genres AS 'ID genre'
              FROM
                  livres l
              JOIN est_ecrit_par ep ON ep.id_livres = l.id_livres
			        JOIN auteurs a ON ep.id_auteurs = a.id_auteurs
              JOIN genres g ON g.id_genres = l.id_genres
              LEFT JOIN emprunts e ON l.id_livres = e.id_livres
              LEFT JOIN utilisateurs u ON u.id_utilisateurs = e.id_utilisateurs
              WHERE e.date_emprunt IS NOT NULL AND e.date_retour IS NULL
              GROUP BY l.id_livres;
            """
        elif filter_type == "late":
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
                          e.date_retour AS 'Date retour',
                          u.nom AS Utilisateur,
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
                  GROUP BY l.id_livres
              ) AS Livres
              WHERE
                  Status = 'En retard';
            """

        return self.database.exec_query(query)

    def insert_book(self, book: Book):
        insert_book_query = f"""
          INSERT INTO livres
            (titre, date_publication, id_genres)
          VALUES
            ('{book.titre}', '{book.date_publication}', {book.genre.id})
        """
        try:
            engine = self.database.getEngine()
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(insert_book_query))
                book_id = result.lastrowid  # Get the auto-generated id_livres

                for auteur in book.auteurs:
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

    def modify_book(self, book: Book):
        delete_authors_query = f"""
          DELETE FROM est_ecrit_par
          WHERE id_livres = {book.id}
        """
        update_book_query = f"""
          UPDATE livres
          SET titre = '{book.titre}', date_publication = '{book.date_publication}', id_genres = {book.genre.id}
          WHERE id_livres = {book.id}
        """
        queries = [delete_authors_query, update_book_query]
        for auteur in book.auteurs:
            query = f"""
            INSERT INTO est_ecrit_par
              (id_auteurs, id_livres)
            VALUES
              ({auteur.id}, {book.id})
          """
            queries.append(query)

        self.database.exec_queries_with_commit(queries)

    def delete_book(self, book_id: int):
        delete_livre_query = f"DELETE FROM livres WHERE id_livres = {book_id}"
        delete_emprunts_query = f"DELETE FROM emprunts WHERE id_livres = {book_id}"
        queries = [delete_livre_query, delete_emprunts_query]
        self.database.exec_queries_with_commit(queries)

    def borrow_book(self, book_id, user_id):
        current_date = datetime.today().strftime("%Y-%m-%d")
        query = f"""
          INSERT INTO emprunts
            (date_emprunt, id_livres, id_utilisateurs)
          VALUES
            ('{current_date}', '{book_id}', {user_id})
        """
        self.database.exec_query_with_commit(query)

    def return_book(self, book_id, user_id):
        current_date = datetime.today().strftime("%Y-%m-%d")
        query = f"""
          UPDATE emprunts
          SET date_retour = '{current_date}'
          WHERE id_livres = {book_id} AND id_utilisateurs = {user_id}
        """
        print("return query: ", query)
        self.database.exec_query_with_commit(query)
