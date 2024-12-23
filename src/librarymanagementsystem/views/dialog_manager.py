import bcrypt
from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.entities.genre import Genre
from librarymanagementsystem.entities.user import User
from librarymanagementsystem.views.author_dialog import AuthorDialog
from librarymanagementsystem.views.book_dialog import BookDialog
from librarymanagementsystem.views.genre_dialog import GenreDialog
from librarymanagementsystem.views.user_dialog import UserDialog


class DialogManager:
    def __init__(self, view):
        self.view = view

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
            return Author(data["prenom"], data["nom"])
        return None

    def add_user(self):
        dialog = UserDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            password = data["password"]
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            return User(
                data["name"],
                data["email"],
                data["phone"],
                data["birthday"],
                data["status"],
                hashed_password,
            )
        return None

    def add_book(self, authors, genres) -> dict | None:
        dialog = BookDialog(authors, genres)
        dialog.populate_fields(None)
        response = dialog.exec()
        if response == QDialog.Accepted:
            return dialog.get_data()
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
            return Author(
                data["prenom"],
                data["nom"],
                author.id,
            )
        return None

    def modify_user(self, user: User):
        dialog = UserDialog()
        dialog.populate_fields(user)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            password = data["password"]
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            return User(
                data["name"],
                data["email"],
                data["phone"],
                data["birthday"],
                data["status"],
                hashed_password,
                user.id,
            )
        return None

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
            return True
        return False

    def delete_user(self, user: User):
        button = QMessageBox.question(
            self.view,
            "Supprimer utilisateur",
            f"Etes-vous sûr de vouloir supprimer l'utilisateur {user.username} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            return True
        return False

    def show_message(self, title: str, message: str):
        QMessageBox.information(self.view, title, message)
        QMessageBox.information(self.view, title, message)
