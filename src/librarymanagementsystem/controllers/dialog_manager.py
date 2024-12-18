from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.bo.author import Author
from librarymanagementsystem.bo.book import Book
from librarymanagementsystem.bo.genre import Genre
from librarymanagementsystem.bo.user import User
from librarymanagementsystem.controllers.database_manager import DatabaseManager
from librarymanagementsystem.views.author_dialog import AuthorDialog
from librarymanagementsystem.views.book_dialog import BookDialog
from librarymanagementsystem.views.genre_dialog import GenreDialog
from librarymanagementsystem.views.user_dialog import UserDialog


class DialogManager:
    def __init__(self, view, database_manager: DatabaseManager):
        self.view = view
        self.database_manager = database_manager

    def add_genre(self) -> Genre | None:
        dialog = GenreDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            new_genre = Genre(data["nom"])
            return new_genre
        return None

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
                data["email"],
                data["statut"],
                data["hash_mot_passe"],
            )
            self.database_manager.insert_user(new_user)

    def add_book(self, authors, genres) -> dict | None:
        dialog = BookDialog(authors, genres)
        dialog.populate_fields(None)
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            return data
        return None

    def modify_book(self, book: Book, authors, genres) -> dict | None:
        dialog = BookDialog(authors, genres)
        dialog.populate_fields(book)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            return data
        return None

    def delete_book(self, book: Book):
        button = QMessageBox.question(
            self.view,
            "Supprimer livre",
            f"Etes-vous sûr de vouloir supprimer le livre {book.title} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            return True
        return False

    def modify_genre(self, genre: Genre) -> Genre | None:
        dialog = GenreDialog()
        dialog.populate_fields(genre)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            existing_genre = Genre(
                data["nom"],
                genre.id,
            )
            return existing_genre
        return None

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
            self.database_manager.modify_author(existing_author)

    def modify_user(self, user: User):
        dialog = UserDialog()
        dialog.populate_fields(user)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            existing_user = User(
                data["nom"],
                data["email"],
                data["statut"],
                data["hash_mot_passe"],
                user.id,
            )
            self.database_manager.modify_user(existing_user)

    def delete_genre(self, genre: Genre) -> bool:
        button = QMessageBox.question(
            self.view,
            "Supprimer genre",
            f"Etes-vous sûr de vouloir supprimer le genre {genre.name} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            return True
        return False

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

    def show_message(self, title: str, message: str):
        QMessageBox.information(self.view, title, message)
        QMessageBox.information(self.view, title, message)
