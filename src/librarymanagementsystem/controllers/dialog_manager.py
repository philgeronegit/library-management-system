from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.controllers.database_manager import DatabaseManager
from librarymanagementsystem.models.author import Author
from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.genre import Genre
from librarymanagementsystem.models.user import User
from librarymanagementsystem.views.author_dialog import AuthorDialog
from librarymanagementsystem.views.book_dialog import BookDialog
from librarymanagementsystem.views.genre_dialog import GenreDialog
from librarymanagementsystem.views.user_dialog import UserDialog


class DialogManager:
    def __init__(self, view, database_manager: DatabaseManager):
        self.view = view
        self.database_manager = database_manager

    def add_genre(self):
        dialog = GenreDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            new_genre = Genre(data["nom"])
            self.database_manager.insert_genre(new_genre)

    def add_author(self):
        dialog = AuthorDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            new_author = Author(data["prenom"], data["nom"])
            self.database_manager.insert_author(new_author)

    def add_user(self):
        dialog = UserDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            new_user = User(
                data["nom"],
                data["contact"],
                data["statut"],
                data["mot_passe"],
            )
            self.database_manager.insert_user(new_user)

    def add_book(self):
        dialog = BookDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            new_book = Book(
                data["titre"], data["auteur"], data["genre"], data["date_publication"]
            )
            self.database_manager.insert_book(new_book)

    def modify_genre(self, genre: Genre):
        dialog = GenreDialog()
        dialog.populate_fields(genre)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            existing_genre = Genre(
                data["nom"],
                genre.id,
            )
            print(data)
            print(existing_genre)
            self.database_manager.modify_genre(existing_genre)

    def modify_author(self, author: Author):
        dialog = AuthorDialog()
        dialog.populate_fields(author)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            existing_author = Author(
                data["prenom"],
                data["nom"],
                author.id,
            )
            print(data)
            print(existing_author)
            self.database_manager.modify_author(existing_author)

    def modify_user(self, user: User):
        dialog = UserDialog()
        dialog.populate_fields(user)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            existing_user = User(
                data["nom"],
                data["contact"],
                data["statut"],
                data["mot_passe"],
                user.id,
            )
            self.database_manager.modify_user(existing_user)

    def modify_book(self, book: Book):
        dialog = BookDialog()
        dialog.populate_fields(book)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            existing_book = Book(
                data["titre"],
                data["auteur"],
                data["genre"],
                data["date_publication"],
                book.id,
            )
            self.database_manager.modify_book(existing_book)

    def delete_genre(self, genre: Genre):
        button = QMessageBox.question(
            self.view,
            "Supprimer genre",
            f"Etes-vous sûr de vouloir supprimer le genre {genre.name} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.database_manager.delete_genre(genre.id)

    def delete_author(self, author: Author):
        button = QMessageBox.question(
            self.view,
            "Supprimer auteur",
            f"Etes-vous sûr de vouloir supprimer l'auteur {author.firstname} {author.lastname} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.database_manager.delete_author(author.id)

    def delete_user(self, user: User):
        button = QMessageBox.question(
            self.view,
            "Supprimer utilisateur",
            f"Etes-vous sûr de vouloir supprimer l'utilisateur {user.username} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.database_manager.delete_user(user.id)

    def delete_book(self, book: Book):
        button = QMessageBox.question(
            self.view,
            "Supprimer livre",
            f"Etes-vous sûr de vouloir supprimer le livre {book.titre} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.database_manager.delete_book(book.id)

    def show_message(self, title: str, message: str):
        QMessageBox.information(self.view, title, message)
        QMessageBox.information(self.view, title, message)
