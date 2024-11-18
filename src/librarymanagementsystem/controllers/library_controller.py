from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.controllers.database_manager import DatabaseManager
from librarymanagementsystem.controllers.dialog_manager import DialogManager
from librarymanagementsystem.controllers.ui_manager import UIManager
from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.table_model import TableModel
from librarymanagementsystem.models.user import User
from librarymanagementsystem.views.ui import LibraryView
from librarymanagementsystem.views.user_dialog import UserDialog


class LibraryController:
    def __init__(self):
        self.view = LibraryView(self)
        self.filter_type = "all"
        self.users_model = None
        self.books_model = None
        self.database = Database()
        self.database_manager = DatabaseManager(self.database)
        self.dialog_manager = DialogManager(self.view, self.database_manager)
        self.ui_manager = UIManager(self.view)
        self.selected_user = None

    def readBooks(self):
        df = self.database_manager.read_books(self.filter_type)
        self.books_model = TableModel(df)

    def readUsers(self):
        df = self.database_manager.read_users()
        self.users_model = TableModel(df)

    def readBorrowRules(self):
        df = self.database_manager.read_borrow_rules()
        self.duree_maximale_emprunt = df.loc[0, "duree_maximale_emprunt"]
        self.penalite_retard = df.loc[0, "penalite_retard"]

    def run(self):
        try:
            self.readBorrowRules()
            self.readBooks()
            self.readUsers()
        except Exception as e:
            print("Impossible de lire les tables {}".format(e))
        self.setup_ui()

        # show statusbar message
        self.show_books_number()
        self.view.show()

    def update_toolbar_actions(self):
        """Update the state of toolbar actions based on the selection"""
        has_selection = self.view.books_table.selectionModel().hasSelection()
        is_admin = self.selected_user and self.selected_user.role == "admin"
        if is_admin:
            self.view.modify_action.setEnabled(has_selection)
            self.view.delete_action.setEnabled(has_selection)

    def setup_ui(self):
        if self.users_model is not None:
            self.ui_manager.setup_users_table(self.users_model)

            rows = self.users_model.rowCount(0)

            for row in range(rows):
                index = self.users_model.index(row, 1)
                value = self.users_model.data(index, Qt.ItemDataRole.DisplayRole)
                self.view.user_combo_box.addItem(value)

        if self.books_model is not None:
            self.ui_manager.setup_books_table(self.books_model)

            # Connect selection change signal to enable/disable toolbar actions
            self.view.books_table.selectionModel().selectionChanged.connect(
                self.update_toolbar_actions
            )

        if self.duree_maximale_emprunt is not None and self.penalite_retard is not None:
            self.view.duree_maximale_emprunt_input.setText(
                str(self.duree_maximale_emprunt)
            )
            self.view.penalite_retard_input.setText(str(self.penalite_retard))

    def show_books_number(self):
        length = 0
        if self.books_model is not None:
            length = self.books_model.rowCount(1)
        self.view.statusBar().showMessage(f"Nombre de livres : {length}")

    def perform_search(self, search_text):
        self.books_model.filterData(search_text)
        self.show_books_number()

    def update_viewport(self):
        # Get the current sort column and order
        sort_column = self.view.books_table.horizontalHeader().sortIndicatorSection()
        sort_order = self.view.books_table.horizontalHeader().sortIndicatorOrder()

        # Read books and update the model
        self.readBooks()
        self.view.books_table.setModel(self.books_model)
        self.view.books_table.resizeColumnsToContents()
        self.view.books_table.viewport().update()

        # Reapply the sort order
        self.view.books_table.sortByColumn(sort_column, sort_order)

        self.show_books_number()

    def filter_change(self, type: str):
        self.filter_type = type
        self.update_viewport()

    def delete_selected_item(self, name, index):
        print(f"Supprimer {name} {index}")
        if name == "books":
            self.delete_book()
        elif name == "users":
            self.delete_user()

    def delete_user(self):
        """Delete a user from the list"""
        user = self.get_selected_user()
        if user is None:
            return

        self.dialog_manager.delete_user(user)
        self.update_viewport()

    def delete_book(self):
        """Delete a book from the list"""
        book = self.get_selected_book()
        if book is None:
            return

        self.dialog_manager.delete_book(book)
        self.update_viewport()

    def login(self):
        dialog = UserDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            user = User(
                data["nom"],
                data["contact"],
                data["statut"],
                data["mot_passe"],
                data["id"],
            )
            # lowercase the username
            if (user.name == "admin") and (user.password == "admin"):
                user.role = "admin"
                self.login_as_user(user)
            else:
                # search user in the pandas dataframe (self.users) with nom and mot_de_passe
                user = self.users[(self.users["nom"] == user.username)]
                if user.empty:
                    QMessageBox.information(
                        self.view, "Utilisateur non trouvé", "Utilisateur non trouvé"
                    )
                else:
                    if user.iloc[0]["mot_de_passe"] != data["mot_de_passe"]:
                        QMessageBox.information(
                            self.view,
                            "Mot de passe incorrect",
                            "Mot de passe incorrect",
                        )
                    else:
                        self.login_as_user(user.iloc[0])

    def login_as_user(self, user: User):
        """Login as a user"""
        self.view.statusBar().showMessage(f"Connecté en tant que {user.name}")
        self.view.setWindowTitle(f"Librairie - Connecté en tant que : {user.name}")
        self.selected_user = user
        self.view.update_user_actions(user)

    def logout(self):
        """Logout the user"""
        self.view.statusBar().showMessage("Déconnecté")
        self.view.setWindowTitle("Librairie")
        self.selected_user = None
        self.view.update_user_actions(None)

    def add_user(self):
        """Add a new user to the list"""
        self.dialog_manager.add_user()
        self.update_viewport()

    def add_book(self):
        """Add a new book to the list"""
        self.dialog_manager.add_book()
        self.update_viewport()

    def borrow_book(self):
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Emprunter ce livre",
            f"Etes-vous sûr de vouloir emprunter ce livre {book}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Emprunter le livre")
            self.database_manager.borrow_book(book.id)

    def restore_books(self):
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Rendre ce livre",
            f"Etes-vous sûr de vouloir rendre ce livre {book}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Livre rendu")

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

    def add_item(self, name):
        if name == "books":
            self.add_book()
        elif name == "users":
            self.add_user()

    def modify_selected_item(self, name, index):
        print(f"Modifier {name} {index}")
        if name == "books":
            self.modify_book()
        elif name == "users":
            self.modify_user()

    def modify_user(self):
        """Modify a user from the list"""
        user = self.get_selected_user()
        if user is None:
            return

        self.dialog_manager.modify_user(user)
        self.update_viewport()

    def modify_book(self):
        """Modify a book from the list"""
        book = self.get_selected_book()
        if book is None:
            return

        self.dialog_manager.modify_book(book)
        self.update_viewport()

    def borrow_book(self, index):
        print(f"Emprunter {index}")
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Emprunter ce livre",
            f"Etes-vous sûr de vouloir emprunter ce livre {book}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Emprunter le livre", book)

    def restore_book(self, index):
        print(f"Restituer {index}")
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Restituer ce livre",
            f"Etes-vous sûr de vouloir restituer ce livre {book}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Restituer le livre", book)

    def get_selected_indexes(self, custom_table_view):
        """Get the selected indexes from the table"""
        indexes = custom_table_view.selectedIndexes()
        if indexes is None or len(indexes) == 0:
            QMessageBox.information(
                self.view, "Pas de sélection", "Pas de lignes sélectionnées"
            )
            return None

        return indexes

    def get_selected_user(self) -> dict:
        """Get the selected user from the table"""
        indexes = self.get_selected_indexes(self.view.users_table)
        if indexes is None:
            return None

        selected_user = None

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                id = self.books_model.data(self.books_model.index(row, 0), role)
                nom = self.books_model.data(self.books_model.index(row, 1), role)
                mot_passe = self.books_model.data(self.books_model.index(row, 2), role)
                contact = self.books_model.data(self.books_model.index(row, 3), role)
                statut = self.books_model.data(self.books_model.index(row, 4), role)
                selected_user = User(nom, contact, statut, mot_passe, id)
                break

        return selected_user

    def get_selected_book(self) -> dict:
        """Get the selected book from the table"""
        indexes = self.get_selected_indexes(self.view.books_table)
        if indexes is None:
            return None

        selected_book = None

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                id = self.books_model.data(self.books_model.index(row, 0), role)
                titre = self.books_model.data(self.books_model.index(row, 1), role)
                auteur = self.books_model.data(self.books_model.index(row, 2), role)
                genre = self.books_model.data(self.books_model.index(row, 3), role)
                date_publication = self.books_model.data(
                    self.books_model.index(row, 4), role
                )
                disponibilite = self.books_model.data(
                    self.books_model.index(row, 5), Qt.ItemDataRole.UserRole
                )
                selected_book = Book(
                    titre, auteur, genre, date_publication, disponibilite, id
                )
                break

        return selected_book

    def save_regles_prets_clicked(self):
        duree = self.view.duree_maximale_emprunt_input.text()
        penalite = self.view.penalite
        print(f"Durée: {duree}")
        print(f"Pénalité: {penalite}")
        self.database_manager.modify_borrow_rules(int(duree), int(penalite))
