from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.repositories.book_repository import BookRepository


class LoanBLL:
    def __init__(self, database: Database):
        self.database = database
        self.book_repository = BookRepository(self.database)

    def borrow_book(self, book_id: int, user_id: int):
        self.book_repository.borrow_book(book_id, user_id)

    def return_book(self, book_id, user_id):
        self.book_repository.return_book(book_id, user_id)
