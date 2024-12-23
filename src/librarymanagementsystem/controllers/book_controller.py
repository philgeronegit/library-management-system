import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.managers.book_manager import BookManager
from librarymanagementsystem.managers.loan_manager import LoanManager
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.utils.constants import BORROWED_BOOKS, USER_ROLE_ADMIN
from librarymanagementsystem.utils.selection import (
    get_column_index_by_name,
    get_integer_value,
    get_model_data,
    get_selected_indexes,
)
from librarymanagementsystem.utils.viewport import update_viewport
from librarymanagementsystem.views.table_model import TableModel


class BookController:
    def __init__(
        self,
        database: Database,
        view,
        author_controller,
        genre_controller,
        user_controller,
        login_controller,
        dialog_manager,
    ):
        self.filter_type = "all"
        self.filter_text = ""
        self.books_model = None
        self.book_manager = BookManager(database)
        self.loan_manager = LoanManager(database)
        self.view = view
        self.author_controller = author_controller
        self.genre_controller = genre_controller
        self.user_controller = user_controller
        self.login_controller = login_controller
        self.dialog_manager = dialog_manager

    def filter_change(self, type: str):
        print(f"Filter change {type}")
        self.filter_type = type
        if type == BORROWED_BOOKS:
            user_id = ""
            if self.login_controller.selected_user is None:
                user_id = ""
            elif self.login_controller.selected_user.role != USER_ROLE_ADMIN:
                user_id = self.login_controller.selected_user.id
            self.read_all(type, user_id)
        else:
            self.read_all()

    def perform_search(self, search_text):
        self.read_all(filter_type="search", filter_text=search_text)

    def user_combo_box_changed(self, index: int):
        id = self.view.user_combo_box.itemData(index)
        self.read_all(filter_type="user", filter_text=id)

    def update_viewport_books(self):
        update_viewport(self.view.books_table, self.books_model)
        self.show_books_number()

    def show_books_number(self):
        length = 0
        if self.books_model is not None:
            length = self.books_model.rowCount(1)
            self.view.statusBar().showMessage(f"Nombre de livres : {length}")

    def read_all(self, filter_type: str = None, filter_text=""):
        type = filter_type or self.filter_type
        print(f"Type {type}")
        df = self.book_manager.read_all(type, filter_text)
        self.books_model = TableModel(df)
        self.update_viewport_books()
        self.show_books_number()

    def delete(self, user_id: int):
        """Delete a book from the list"""
        book = self.get_selected_book()
        if book is None:
            return

        to_delete = self.dialog_manager.delete_book(book)
        if to_delete:
            self.book_manager.delete(book.id, user_id)
            self.read_all()

    def get_selected_book(self) -> Book | None:
        """Get the selected book from the table"""
        indexes = get_selected_indexes(self.view.books_table)
        if indexes is None:
            return None

        selected_book = None

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                books_model = self.books_model
                id = books_model.data(books_model.index(row, 0), role)
                title = books_model.data(books_model.index(row, 1), role)
                publication_date = books_model.data(books_model.index(row, 4), role)
                index = get_column_index_by_name(books_model, "ID auteurs")
                author_ids = books_model.data(
                    books_model.index(row, index), role
                ).split(",")
                author_ids = [int(auteur_id) for auteur_id in author_ids]

                genre_id = get_model_data(books_model, row, "ID genre")
                borrowed_date = get_model_data(books_model, row, "Date emprunt")
                return_date = get_model_data(books_model, row, "Date retour")
                creation_date = get_model_data(books_model, row, "Date création")
                created_by = get_model_data(books_model, row, "Créé par")
                modification_date = get_model_data(
                    books_model, row, "Date modification"
                )
                modified_by = get_model_data(books_model, row, "Modifié par")
                deletion_date = get_model_data(books_model, row, "Date suppression")
                deleted_by = get_integer_value(
                    get_model_data(books_model, row, "Supprimé par")
                )

                selected_book = self.create_book(
                    title,
                    author_ids,
                    genre_id,
                    publication_date,
                    id=int(id),
                    borrowed_date=borrowed_date,
                    return_date=return_date,
                    creation_date=creation_date,
                    created_by=created_by,
                    modification_date=modification_date,
                    modified_by=modified_by,
                    deletion_date=deletion_date,
                    deleted_by=deleted_by,
                )
                print(selected_book)
                break

        return selected_book

    def create_book(
        self,
        title: str,
        author_ids: list[int],
        genre_id: int,
        publication_date: datetime,
        borrowed_date: datetime = None,
        return_date: datetime = None,
        creation_date: datetime = None,
        created_by: int = None,
        modification_date: datetime = None,
        modified_by: int = None,
        deletion_date: datetime = None,
        deleted_by: int = None,
        id: int = None,
    ) -> Book:
        authors = []
        for author_id in author_ids:
            author = self.author_controller.find_author(int(author_id))
            authors.append(author)
        genre = self.genre_controller.find_genre(int(genre_id))
        created_by_user = self.user_controller.find_user(created_by)
        modified_by_user = self.user_controller.find_user(modified_by)
        deleted_by_user = self.user_controller.find_user(deleted_by)
        return Book(
            title,
            authors,
            genre,
            publication_date,
            id=id,
            borrowing_date=borrowed_date,
            return_date=return_date,
            creation_date=creation_date,
            added_by=created_by_user,
            modification_date=modification_date,
            modified_by=modified_by_user,
            deletion_date=deletion_date,
            deleted_by=deleted_by_user,
        )

    def modify(self, user_id: int):
        """Modify a book from the list"""
        book = self.get_selected_book()
        if book is None:
            return

        book_data = self.dialog_manager.modify_book(
            book,
            self.author_controller.authors_model,
            self.genre_controller.genres_model,
        )
        if book_data is None:
            return

        existing_book = self.create_book(
            book_data["title"],
            book_data["author_ids"],
            book_data["genre_id"],
            book_data["publication_date"],
            id=book_data["id"],
        )
        self.book_manager.modify(existing_book, user_id)
        self.read_all()

    def borrow_book(self):
        """Borrow a book from the list"""
        selected_user = self.login_controller.selected_user
        print(f"Selectedd user {selected_user}")
        if selected_user is None or selected_user.role == USER_ROLE_ADMIN:
            QMessageBox.information(
                self.view,
                "Utilisateur",
                "Veuillez vous connecter en tant qu'utilisateur",
            )
            return

        user_id = selected_user.id
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Emprunter ce livre",
            f"Etes-vous sûr de vouloir emprunter ce livre {book.title} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            self.loan_manager.borrow_book(book.id, user_id)
            self.read_all()

    def restore_book(self):
        """Restore books from the list"""
        selected_user = self.login_controller.selected_user
        if selected_user is None:
            QMessageBox.information(
                self.view,
                "Utilisateur",
                "Veuillez vous connecter en tant qu'utilisateur",
            )
            return
        user_id = selected_user.id
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Rendre ce livre",
            f"Etes-vous sûr de vouloir rendre ce livre {book.title} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            self.loan_manager.return_book(book.id, user_id)
            self.read_all()

    def reserve_book(self):
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Réserver ce livre",
            f"Etes-vous sûr de vouloir réserver ce livre {book}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Livre réservé")

    def add(self, user_id: int):
        """Add a new book to the list"""
        book_data = self.dialog_manager.add_book(
            self.author_controller.authors_model, self.genre_controller.genres_model
        )
        if book_data is None:
            return

        new_book = self.create_book(
            book_data["title"],
            book_data["author_ids"],
            book_data["genre_id"],
            book_data["publication_date"],
        )
        if new_book is None:
            return

        self.book_manager.insert(new_book, user_id)
        self.read_all()
