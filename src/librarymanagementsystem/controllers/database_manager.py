from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.models.author import Author
from librarymanagementsystem.models.user import User


class DatabaseManager:
    def __init__(self, database: Database):
        self.database = database

    def read_users(self):
        query = "SELECT * FROM utilisateurs;"
        return self.database.exec_query(query)

    def read_authors(self):
        query = "SELECT * FROM auteurs;"
        return self.database.exec_query(query)

    def read_borrow_rules(self):
        query = "SELECT * FROM regles_prets;"
        return self.database.exec_query(query)

    def delete_author(self, author_id: int):
        query = f"DELETE FROM auteurs WHERE id_auteurs = {author_id}"
        self.database.exec_query_with_commit(query)

    def delete_user(self, user_id: int):
        query = f"DELETE FROM utilisateurs WHERE id_utilisateurs = {user_id}"
        self.database.exec_query_with_commit(query)

    def insert_author(self, author: Author):
        query = f"""
          INSERT INTO auteurs
            (prenom, nom)
          VALUES
            ('{author.firstname}', '{author.lastname}')
        """
        self.database.exec_query_with_commit(query)

    def insert_user(self, user: User):
        query = f"""
          INSERT INTO utilisateurs
            (nom, contact, statut, mot_passe)
          VALUES
            ('{user.username}', '{user.email}', '{user.status}', '{user.password}')
        """
        self.database.exec_query_with_commit(query)

    def modify_author(self, author: Author):
        query = f"""
          UPDATE auteurs
          SET prenom = '{author.firstname}', nom = '{author.lastname}'
          WHERE id_auteurs = {author.id}
        """
        self.database.exec_query_with_commit(query)

    def modify_user(self, user: User):
        query = f"""
          UPDATE utilisateurs
          SET nom = '{user.username}', contact = '{user.email}', statut = '{user.status}', mot_passe = '{user.password}'
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
