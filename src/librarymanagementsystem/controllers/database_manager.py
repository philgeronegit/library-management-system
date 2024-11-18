from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.user import User


class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def read_books(self, filter_type="all"):
        query = "SELECT * FROM livres;"
        if filter_type == "available":
            query = "SELECT * FROM livres WHERE disponibilite = 1;"
        elif filter_type == "borrowed":
            query = "SELECT * FROM livres WHERE disponibilite = 0;"
        elif filter_type == "late":
            query = """
              SELECT
              livres.id_livres AS ID,
              livres.titre AS Titre,
              livres.auteur AS Auteur,
              livres.genre AS Genre,
              livres.date_publication AS 'Date publication',
              livres.disponibilite AS Disponibilité,
              emprunts.date_emprunt As 'Date emprunt',
              emprunts.date_retour AS 'Date retour',
              utilisateurs.nom AS Utilisateur
              FROM livres
              LEFT JOIN emprunts ON livres.id_livres = emprunts.livre_id_livres
              LEFT JOIN utilisateurs ON utilisateurs.id_utilisateurs = emprunts.utilisateur_id_utilisateurs;
            """
        return self.database.exec_query(query)

    def read_users(self):
        query = "SELECT * FROM utilisateurs;"
        return self.database.exec_query(query)

    def read_borrow_rules(self):
        query = "SELECT * FROM regles_prets;"
        return self.database.exec_query(query)

    def delete_book(self, book_id: int):
        query = f"DELETE FROM livres WHERE id_livres = {book_id}"
        self.database.exec_query_with_commit(query)

    def delete_user(self, user_id: int):
        query = f"DELETE FROM utilisateurs WHERE id_utilisateurs = {user_id}"
        self.database.exec_query_with_commit(query)

    def insert_user(self, user: User):
        query = f"""
          INSERT INTO utilisateurs
            (nom, contact, statut, mot_passe)
          VALUES
            ('{user.nom}', '{user.contact}', '{user.statut}', '{user.mot_passe}')
        """
        self.database.exec_query_with_commit(query)

    def insert_book(self, book: Book):
        query = f"""
          INSERT INTO livres
            (titre, auteur, genre, date_publication, disponibilite)
          VALUES
            ('{book.titre}', '{book.auteur}', '{book.genre}', '{book.date_publication}', {book.disponibilite})
        """
        self.database.exec_query_with_commit(query)

    def modify_book(self, book: Book):
        query = f"""
          UPDATE livres
          SET titre = '{book.titre}', auteur = '{book.auteur}', genre = '{book.genre}', date_publication = '{book.date_publication}', disponibilite = {book.disponibilite}
          WHERE id_livres = {book.id}
        """
        self.database.exec_query_with_commit(query)

    def modify_user(self, user: User):
        query = f"""
          UPDATE utilisateurs
          SET nom = '{user.nom}', contact = '{user.contact}', statut = '{user.statut}', mot_passe = '{user.mot_passe}'
          WHERE id_utilisateurs = {user.id}
        """
        self.database.exec_query_with_commit(query)

    def modify_borrow_rules(self, duree_maximale_emprunt: int, penalite_par_jour: int):
        query = f"""
          UPDATE regles_prets
          SET duree = {duree_maximale_emprunt}, penalite = {penalite_par_jour}
          WHERE id_regles_prets = 1
        """
        self.database.exec_query_with_commit(query)
