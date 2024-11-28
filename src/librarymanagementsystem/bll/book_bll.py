from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.dal.book_dal import BookDAL


class BookBLL:
    def __init__(self, database: Database):
        self.database = database
        self.book_dal = BookDAL(self.database)

    def read_books(self, filter_type: str, filter_text=""):
        return self.book_dal.read_books(filter_type, filter_text)

    def modify_book(self, book, user_id):
        self.book_dal.modify_book(book, user_id)

    def delete_book(self, book_id, user_id):
        self.book_dal.delete_book(book_id, user_id)

    def insert_book(self, book, user_id):
        self.book_dal.insert_book(book, user_id)
