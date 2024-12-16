from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.entities.genre import Genre


class GenreRepository:
    def __init__(self, database: Database):
        self.database = database

    def read_genres(self):
        query = "SELECT * FROM genres;"
        return self.database.exec_query(query)

    def insert_genre(self, genre: Genre):
        query = f"""
          INSERT INTO genres
            (nom)
          VALUES
            ('{genre.name}')
        """
        self.database.exec_query_with_commit(query)

    def modify_genre(self, genre: Genre):
        query = f"""
          UPDATE genres
          SET nom = '{genre.name}'
          WHERE id_genres = {genre.id}
        """
        self.database.exec_query_with_commit(query)

    def delete_genre(self, genre_id: int):
        query = f"DELETE FROM genres WHERE id_genres = {genre_id}"
        self.database.exec_query_with_commit(query)
