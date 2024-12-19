from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.repositories.database import Database


class AuthorRepository:
    def __init__(self, database: Database):
        self.database = database

    def read_all(self):
        query = "SELECT * FROM auteurs;"
        return self.database.exec_query(query)

    def insert(self, author: Author):
        query = f"""
          INSERT INTO auteurs
            (prenom, nom)
          VALUES
            ('{author.firstname}', '{author.lastname}')
        """
        self.database.exec_query_with_commit(query)

    def modify(self, author: Author):
        query = f"""
          UPDATE auteurs
          SET prenom = '{author.firstname}', nom = '{author.lastname}'
          WHERE id_auteurs = {author.id}
        """
        self.database.exec_query_with_commit(query)

    def delete(self, author_id: int):
        query = f"DELETE FROM auteurs WHERE id_auteurs = {author_id}"
        self.database.exec_query_with_commit(query)
