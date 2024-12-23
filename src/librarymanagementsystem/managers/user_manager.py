from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.repositories.user_repository import UserRepository


class UserManager:
    def __init__(self, database: Database):
        self.user_repository = UserRepository(database)

    def read_all(self):
        return self.user_repository.read_all()

    def modify(self, book):
        self.user_repository.modify(book)

    def change_password(self, user_id: int, password: str):
        self.user_repository.change_password(user_id, password)

    def delete(self, book_id):
        self.user_repository.delete(book_id)

    def insert(self, book):
        self.user_repository.insert(book)
