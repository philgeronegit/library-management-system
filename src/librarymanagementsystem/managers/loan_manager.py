from librarymanagementsystem.repositories.book_repository import BookRepository
from librarymanagementsystem.repositories.database import Database


class LoanManager:
    def __init__(self, database: Database):
        self.book_repository = BookRepository(database)

    def borrow_book(self, book_id: int, user_id: int):
        self.book_repository.borrow_book(book_id, user_id)

    def return_book(self, book_id: int, user_id: int):
        self.book_repository.return_book(book_id, user_id)
