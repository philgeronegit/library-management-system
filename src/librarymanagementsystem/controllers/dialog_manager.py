from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.user import User
from librarymanagementsystem.views.book_dialog import BookDialog
from librarymanagementsystem.views.user_dialog import UserDialog


class DialogManager:
    def __init__(self, view, database_manager):
        self.view = view
        self.database_manager = database_manager

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
                data["titre"],
                data["auteur"],
                data["genre"],
                data["date_publication"],
                data["disponibilite"],
            )
            self.database_manager.insert_book(new_book)

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
                data["disponibilite"],
                book.id,
            )
            self.database_manager.modify_book(existing_book)

    def delete_user(self, user: User):
        button = QMessageBox.question(
            self.view,
            "Supprimer utilisateur",
            f"Etes-vous sûr de vouloir supprimer l'utilisateur {user.nom}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.database_manager.delete_user(user.id)

    def delete_book(self, book: Book):
        button = QMessageBox.question(
            self.view,
            "Supprimer livre",
            f"Etes-vous sûr de vouloir supprimer le livre {book.titre}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.database_manager.delete_book(book.id)

    def show_message(self, title: str, message: str):
        QMessageBox.information(self.view, title, message)
        QMessageBox.information(self.view, title, message)