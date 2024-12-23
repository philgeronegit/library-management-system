from librarymanagementsystem.entities.genre import Genre
from librarymanagementsystem.repositories.database import Database


class GenreRepository:
    def __init__(self, database: Database):
        self.database = database

    def read_all(self):
        query = "SELECT * FROM genres;"
        return self.database.exec_query(query)

    def insert(self, genre: Genre):
        query = f"""
          INSERT INTO genres
            (nom)
          VALUES
            ('{genre.name}')
        """
        self.database.exec_query_with_commit(query)

    def modify(self, genre: Genre):
        query = f"""
          UPDATE genres
          SET nom = '{genre.name}'
          WHERE id_genres = {genre.id}
        """
        self.database.exec_query_with_commit(query)

    def delete(self, genre_id: int):
        query = f"DELETE FROM genres WHERE id_genres = {genre_id}"
        self.database.exec_query_with_commit(query)
