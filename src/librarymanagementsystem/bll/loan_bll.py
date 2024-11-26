from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.dal.book_dal import BookDAL


class LoanBLL:
    def __init__(self, database: Database):
        self.database = database
        self.book_dal = BookDAL(self.database)

    def borrow_book(self, book_id: int, user_id: int):
        self.book_dal.borrow_book(book_id, user_id)

    def return_book(self, book_id, user_id):
        self.book_dal.return_book(book_id, user_id)
