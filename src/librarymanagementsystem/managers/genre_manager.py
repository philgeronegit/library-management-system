from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.repositories.genre_repository import GenreRepository


class GenreManager:
    def __init__(self, database: Database):
        self.genre_repository = GenreRepository(database)

    def read_all(self):
        return self.genre_repository.read_all()

    def modify(self, book):
        self.genre_repository.modify(book)

    def delete(self, book_id):
        self.genre_repository.delete(book_id)

    def insert(self, book):
        self.genre_repository.insert(book)
