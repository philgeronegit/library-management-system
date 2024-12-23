from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.repositories.user_repository import UserRepository


class UserManager:
    def __init__(self, database: Database):
        self.genre_repository = UserRepository(database)

    def read_all(self):
        return self.genre_repository.read_all()

    def modify(self, book):
        self.genre_repository.modify(book)

    def delete(self, book_id):
        self.genre_repository.delete(book_id)

    def insert(self, book):
        self.genre_repository.insert(book)
