from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.bll.book_bll import BookBLL
from librarymanagementsystem.bll.loan_bll import LoanBLL
from librarymanagementsystem.controllers.database import Database
from librarymanagementsystem.controllers.database_manager import DatabaseManager
from librarymanagementsystem.controllers.dialog_manager import DialogManager
from librarymanagementsystem.controllers.genre_dal import GenreDAL
from librarymanagementsystem.controllers.ui_manager import UIManager
from librarymanagementsystem.models.author import Author
from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.genre import Genre
from librarymanagementsystem.models.table_model import TableModel
from librarymanagementsystem.models.user import User
from librarymanagementsystem.views.components.custom_table_view import CustomTableView
from librarymanagementsystem.views.login_dialog import LoginDialog
from librarymanagementsystem.views.ui import LibraryView


class LibraryController:
    def __init__(self):
        self.view = LibraryView(self)
        self.filter_type = "all"
        self.filter_text = ""
        self.books_model = None
        self.users_model = None
        self.authors_model = None
        self.genres_model = None
        self.database = Database()
        self.database_manager = DatabaseManager(self.database)
        self.genre_dal = GenreDAL(self.database)
        self.book_bll = BookBLL(self.database)
        self.loan_bll = LoanBLL(self.database)
        self.dialog_manager = DialogManager(self.view, self.database_manager)
        self.ui_manager = UIManager(self.view)
        self.selected_user = None
        self.duree_maximale_emprunt = None
        self.penalite_retard = None

        user = User("John Doe", "admin", "actif", "admin", 1, role="user")
        # user = User("admin", "admin", "actif", "admin", 1000, role="admin")
        self.login_as_user(user)

    def read_books(self):
        df = self.book_bll.read_books(filter_type=self.filter_type)
        self.books_model = TableModel(df)
        self.show_books_number()

    def read_users(self):
        df = self.database_manager.read_users()
        self.users_model = TableModel(df)

    def read_authors(self):
        df = self.database_manager.read_authors()
        self.authors_model = TableModel(df)

    def read_genres(self):
        df = self.genre_dal.read_genres()
        self.genres_model = TableModel(df)

    def read_borrow_rules(self):
        df = self.database_manager.read_borrow_rules()
        self.duree_maximale_emprunt = df.loc[0, "duree_maximale_emprunt"]
        self.penalite_retard = df.loc[0, "penalite_retard"]

    def run(self):
        try:
            self.read_borrow_rules()
            self.read_books()
            self.read_users()
            self.read_authors()
            self.read_genres()
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
        self.view.borrow_action.setEnabled(has_selection)
        self.view.restore_action.setEnabled(has_selection)
        self.view.reserve_action.setEnabled(has_selection)
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

        if self.authors_model is not None:
            self.ui_manager.setup_authors_table(self.authors_model)

        if self.genres_model is not None:
            self.ui_manager.setup_genres_table(self.genres_model)

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
        df = self.book_bll.read_books(filter_type="search", filter_text=search_text)
        if df.empty:
            print("Pas de résultats")
            return

        self.books_model = TableModel(df)
        self.update_viewport_books()

    def update_viewport(self, table_view, model):
        # Get the current sort column and order
        sort_column = table_view.horizontalHeader().sortIndicatorSection()
        sort_order = table_view.horizontalHeader().sortIndicatorOrder()

        # Set the model to the table view
        table_view.setModel(model)
        table_view.resizeColumnsToContents()
        table_view.viewport().update()

        # Reapply the sort order
        table_view.sortByColumn(sort_column, sort_order)

    def update_viewport_genres(self):
        self.update_viewport(self.view.genres_table, self.genres_model)

    def update_viewport_authors(self):
        self.update_viewport(self.view.authors_table, self.authors_model)

    def update_viewport_books(self):
        self.update_viewport(self.view.books_table, self.books_model)
        self.show_books_number()

    def update_viewport_users(self):
        self.update_viewport(self.view.users_table, self.users_model)

    def filter_change(self, type: str):
        print(f"Filter change {type}")
        self.filter_type = type
        self.read_books()
        self.update_viewport_books()

    def delete_selected_item(self, name: str, index: int):
        """Delete the selected item from the table"""
        if name == "books":
            self.delete_book()
        elif name == "genres":
            self.delete_genre()
        elif name == "authors":
            self.delete_author()
        elif name == "users":
            self.delete_user()

    def delete_genre(self):
        """Delete a genre from the list"""
        genre = self.get_selected_genre()
        if genre is None:
            return

        to_delete = self.dialog_manager.delete_genre(genre)
        if not to_delete:
            return
        self.genre_dal.delete_genre(genre.id)
        self.read_genres()
        self.update_viewport_genres()

    def delete_author(self):
        """Delete a author from the list"""
        author = self.get_selected_author()
        if author is None:
            return

        self.dialog_manager.delete_author(author)
        self.read_authors()
        self.update_viewport_authors()

    def delete_user(self):
        """Delete a user from the list"""
        user = self.get_selected_user()
        if user is None:
            return

        self.dialog_manager.delete_user(user)
        self.read_users()
        self.update_viewport_users()

    def delete_book(self):
        """Delete a book from the list"""
        book = self.get_selected_book()
        if book is None:
            return

        to_delete = self.dialog_manager.delete_book(book)
        if to_delete:
            self.book_bll.delete_book(book.id)
        self.read_books()
        self.update_viewport_books()

    def login(self):
        dialog = LoginDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            username = data["nom"]
            password = data["hash_mot_passe"]
            if (username == "admin") and (password == "admin"):
                user = User(username, "admin", "actif", password, role="admin")
                self.login_as_user(user)
            else:
                users_df = self.users_model.raw_data
                user = users_df[(users_df["nom"] == username)]
                if user.empty:
                    QMessageBox.information(
                        self.view, "Utilisateur", "Utilisateur non trouvé"
                    )
                else:
                    user_password = user.iloc[0]["hash_mot_passe"]
                    if user_password != user_password:
                        QMessageBox.information(
                            self.view,
                            "Utilisateur",
                            "Mot de passe incorrect",
                        )
                    else:
                        status = user.iloc[0]["statut"]
                        if status == "actif":
                            user = User(
                                user.iloc[0]["nom"],
                                user.iloc[0]["email"],
                                user.iloc[0]["statut"],
                                user.iloc[0]["hash_mot_passe"],
                                user.iloc[0]["id_utilisateurs"],
                                user.iloc[0]["role"],
                            )
                            self.login_as_user(user)
                        elif status == "inactif":
                            QMessageBox.information(
                                self.view,
                                "Utilisateur",
                                "Utilisateur inactif",
                            )
                        elif status == "en-attente":
                            QMessageBox.information(
                                self.view,
                                "Utilisateur",
                                "Utilisateur en attente",
                            )

    def login_as_user(self, user: User):
        """Login as a user"""
        self.view.statusBar().showMessage(f"Connecté en tant que {user.username}")
        self.view.setWindowTitle(f"Librairie - Connecté en tant que : {user.username}")
        self.selected_user = user
        self.view.update_user_actions(user)

    def logout(self):
        """Logout the user"""
        self.view.statusBar().showMessage("Déconnecté")
        self.view.setWindowTitle("Librairie")
        self.selected_user = None
        self.view.update_user_actions(None)

    def add_genre(self):
        """Add a new genre to the list"""
        new_genre = self.dialog_manager.add_genre()
        if new_genre is None:
            return
        self.genre_dal.insert_genre(new_genre)
        self.read_genres()
        self.update_viewport_genres()

    def add_author(self):
        """Add a new author to the list"""
        self.dialog_manager.add_author()
        self.read_authors()
        self.update_viewport_authors()

    def add_user(self):
        """Add a new user to the list"""
        self.dialog_manager.add_user()
        self.read_users()
        self.update_viewport_users()

    def add_book(self):
        """Add a new book to the list"""
        book_data = self.dialog_manager.add_book(self.authors_model, self.genres_model)
        if book_data is None:
            return
        new_book = self.create_book(
            book_data["titre"],
            book_data["auteur_ids"],
            book_data["genre_id"],
            book_data["date_publication"],
        )
        if new_book is None:
            return
        self.book_bll.insert_book(new_book)
        self.read_books()
        self.update_viewport_books()

    def modify_book(self):
        """Modify a book from the list"""
        book = self.get_selected_book()
        if book is None:
            return

        book_data = self.dialog_manager.modify_book(
            book, self.authors_model, self.genres_model
        )
        if book_data is None:
            return
        existing_book = self.create_book(
            book_data["titre"],
            book_data["auteur_ids"],
            book_data["genre_id"],
            book_data["date_publication"],
            id=book_data["id"],
        )
        self.book_bll.modify_book(existing_book)
        self.read_books()
        self.update_viewport_books()

    def borrow_book(self):
        """Borrow a book from the list"""
        if self.selected_user is None or self.selected_user.role == "admin":
            QMessageBox.information(
                self.view,
                "Utilisateur",
                "Veuillez vous connecter en tant qu'utilisateur",
            )
            return

        user_id = self.selected_user.id
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Emprunter ce livre",
            f"Etes-vous sûr de vouloir emprunter ce livre {book.titre} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            self.loan_bll.borrow_book(book.id, user_id)
            self.read_books()
            self.update_viewport_books()

    def restore_book(self):
        """Restore books from the list"""
        if self.selected_user is None:
            QMessageBox.information(
                self.view,
                "Utilisateur",
                "Veuillez vous connecter en tant qu'utilisateur",
            )
            return
        user_id = self.selected_user.id
        book = self.get_selected_book()
        if book is None:
            return

        button = QMessageBox.question(
            self.view,
            "Rendre ce livre",
            f"Etes-vous sûr de vouloir rendre ce livre {book.titre} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if button == QMessageBox.StandardButton.Yes:
            self.loan_bll.return_book(book.id, user_id)
            self.read_books()
            self.update_viewport_books()

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

    def add_item(self, name: str):
        if name == "books":
            self.add_book()
        elif name == "genres":
            self.add_genre()
        elif name == "authors":
            self.add_author()
        elif name == "users":
            self.add_user()

    def modify_selected_item(self, name: str, index: int):
        if name == "books":
            self.modify_book()
        elif name == "genres":
            self.modify_genre()
        elif name == "authors":
            self.modify_author()
        elif name == "users":
            self.modify_user()

    def modify_genre(self):
        """Modify a author from the list"""
        genre = self.get_selected_genre()
        if genre is None:
            return

        existing_genre = self.dialog_manager.modify_genre(genre)
        if existing_genre is None:
            return
        self.genre_dal.modify_genre(existing_genre)
        self.read_genres()
        self.update_viewport_genres()

    def modify_author(self):
        """Modify a quthor from the list"""
        author = self.get_selected_author()
        if author is None:
            return

        self.dialog_manager.modify_author(author)
        self.read_authors()
        self.update_viewport_authors()

    def modify_user(self):
        """Modify a user from the list"""
        user = self.get_selected_user()
        if user is None:
            return

        self.dialog_manager.modify_user(user)
        self.read_users()
        self.update_viewport_users()

    def get_selected_indexes(self, custom_table_view: CustomTableView):
        """Get the selected indexes from the table"""
        indexes = custom_table_view.selectedIndexes()
        if indexes is None or len(indexes) == 0:
            QMessageBox.information(
                self.view, "Pas de sélection", "Pas de lignes sélectionnées"
            )
            return None

        return indexes

    def get_selected_genre(self) -> dict:
        """Get the selected genre from the table"""
        indexes = self.get_selected_indexes(self.view.genres_table)
        if indexes is None:
            return None

        selected_genre = None

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                id = self.genres_model.data(self.genres_model.index(row, 0), role)
                nom = self.genres_model.data(self.genres_model.index(row, 1), role)
                selected_genre = Genre(nom, id)
                break

        return selected_genre

    def get_selected_author(self) -> dict:
        """Get the selected author from the table"""
        indexes = self.get_selected_indexes(self.view.authors_table)
        if indexes is None:
            return None

        selected_author = None

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                id = self.authors_model.data(self.authors_model.index(row, 0), role)
                nom = self.authors_model.data(self.authors_model.index(row, 1), role)
                prenom = self.authors_model.data(self.authors_model.index(row, 2), role)
                selected_author = Author(prenom, nom, id)
                break

        return selected_author

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

                id = self.users_model.data(self.users_model.index(row, 0), role)
                nom = self.users_model.data(self.users_model.index(row, 1), role)
                mot_passe = self.users_model.data(self.users_model.index(row, 2), role)
                contact = self.users_model.data(self.users_model.index(row, 3), role)
                statut = self.users_model.data(self.users_model.index(row, 4), role)
                selected_user = User(nom, contact, statut, mot_passe, id)
                break

        return selected_user

    def get_column_names(self, model):
        column_names = []
        for column in range(model.columnCount(0)):
            column_name = model.headerData(
                column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            column_names.append(column_name)
        return column_names

    def get_column_index_by_name(self, model, column_name: str):
        for column in range(model.columnCount(0)):
            if (
                model.headerData(
                    column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
                )
                == column_name
            ):
                return column
        return -1

    def find_author(self, id: int) -> Author | None:
        author_df = self.authors_model.raw_data[
            self.authors_model.raw_data["id_auteurs"] == id
        ]
        if author_df.empty:
            return None
        prenom = author_df["prenom"].values[0]
        nom = author_df["nom"].values[0]
        author = Author(
            prenom,
            nom,
            id,
        )
        return author

    def find_genre(self, id: int) -> Genre | None:
        genre_df = self.genres_model.raw_data[
            self.genres_model.raw_data["id_genres"] == id
        ]
        if genre_df.empty:
            return None
        genre = Genre(
            genre_df["nom"].values[0],
            id,
        )
        return genre

    def get_selected_book(self) -> Book | None:
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
                date_publication = self.books_model.data(
                    self.books_model.index(row, 4), role
                )
                index = self.get_column_index_by_name(self.books_model, "ID auteurs")
                auteur_ids = self.books_model.data(
                    self.books_model.index(row, index), role
                ).split(",")
                auteur_ids = [int(auteur_id) for auteur_id in auteur_ids]
                index = self.get_column_index_by_name(self.books_model, "ID genre")
                genre_id = self.books_model.data(
                    self.books_model.index(row, index), role
                )
                index = self.get_column_index_by_name(self.books_model, "Date emprunt")
                date_emprunt = self.books_model.data(
                    self.books_model.index(row, index), role
                )
                index = self.get_column_index_by_name(self.books_model, "Date retour")
                date_retour = self.books_model.data(
                    self.books_model.index(row, index), role
                )
                selected_book = self.create_book(
                    titre,
                    auteur_ids,
                    genre_id,
                    date_publication,
                    id=int(id),
                    date_emprunt=date_emprunt,
                    date_retour=date_retour,
                )
                print(f"Selected book: {selected_book}")
                break

        return selected_book

    def create_book(
        self,
        titre: str,
        auteur_ids: list[int],
        genre_id: int,
        date_publication: str,
        date_emprunt: str = None,
        date_retour: str = None,
        id: int = None,
    ) -> Book:
        auteurs = []
        for auteur_id in auteur_ids:
            auteur = self.find_author(int(auteur_id))
            auteurs.append(auteur)
        genre = self.find_genre(int(genre_id))
        return Book(titre, auteurs, genre, date_publication, id=id)

    def save_regles_prets_clicked(self):
        duree = self.view.duree_maximale_emprunt_input.text().strip()
        penalite = self.view.penalite_retard_input.text().strip()
        print(f"Durée: {duree}")
        print(f"Pénalité: {penalite}")
        self.database_manager.modify_borrow_rules(int(duree), int(penalite))
        self.read_books()
        self.update_viewport_books()
