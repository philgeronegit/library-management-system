from librarymanagementsystem.entities.user import User
from librarymanagementsystem.repositories.database import Database


class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    def read_all(self):
        query = "SELECT * FROM utilisateurs;"
        return self.database.exec_query(query)

    def insert(self, user: User):
        query = f"""
          INSERT INTO utilisateurs
            (nom, email, date_naissance, statut, hash_mot_passe)
          VALUES
            ('{user.username}', '{user.email}', '{user.birthday}', '{user.status}', '{user.password}')
        """
        self.database.exec_query_with_commit(query)

    def modify(self, user: User):
        query = f"""
          UPDATE utilisateurs
          SET nom = '{user.username}', email = '{user.email}', statut = '{user.status}', hash_mot_passe = '{user.password}'
          WHERE id_utilisateurs = {user.id}
        """
        self.database.exec_query_with_commit(query)

    def delete(self, user_id: int):
        query = f"DELETE FROM utilisateurs WHERE id_utilisateurs = {user_id}"
        self.database.exec_query_with_commit(query)