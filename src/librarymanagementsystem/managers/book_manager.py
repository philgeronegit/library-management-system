from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.repositories.book_repository import BookRepository
from librarymanagementsystem.repositories.database import Database


class BookManager:
    def __init__(self, database: Database):
        self.book_repository = BookRepository(database)

    def read_all(self, filter_type: str, filter_text=""):
        return self.book_repository.read_all(filter_type, filter_text)

    def modify(self, book: Book, user_id: int):
        self.book_repository.modify(book, user_id)

    def delete(self, book_id: int, user_id: int):
        self.book_repository.delete(book_id, user_id)

    def insert(self, book: Book, user_id: int):
        self.book_repository.insert(book, user_id)
