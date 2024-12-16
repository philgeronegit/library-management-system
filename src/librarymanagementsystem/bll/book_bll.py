from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.repositories.book_repository import BookRepository


class BookBLL:
    def __init__(self, database: Database):
        self.database = database
        self.book_repository = BookRepository(self.database)

    def read_books(self, filter_type: str, filter_text=""):
        return self.book_repository.read_books(filter_type, filter_text)

    def modify_book(self, book, user_id):
        self.book_repository.modify_book(book, user_id)

    def delete_book(self, book_id, user_id):
        self.book_repository.delete_book(book_id, user_id)

    def insert_book(self, book, user_id):
        self.book_repository.insert_book(book, user_id)
