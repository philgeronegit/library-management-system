from PyQt6.QtCore import Qt

from librarymanagementsystem.controllers.author_controller import AuthorController
from librarymanagementsystem.controllers.book_controller import BookController
from librarymanagementsystem.controllers.borrow_rules_controller import (
    BorrowRulesController,
)
from librarymanagementsystem.controllers.genre_controller import GenreController
from librarymanagementsystem.controllers.login_controller import LoginController
from librarymanagementsystem.controllers.user_controller import UserController
from librarymanagementsystem.entities.user import User
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.utils.viewport import setup_table
from librarymanagementsystem.views.dialog_manager import DialogManager
from librarymanagementsystem.views.ui import LibraryView


class LibraryApp:
    def __init__(self, role):
        self.role = role
        self.view = LibraryView(self)
        self.dialog_manager = DialogManager(self.view)
        self.database = Database()
        self.author_controller = AuthorController(
            self.database, self.view, self.dialog_manager
        )
        self.genre_controller = GenreController(
            self.database, self.view, self.dialog_manager
        )
        self.user_controller = UserController(
            self.database, self.view, self.dialog_manager
        )
        self.login_controller = LoginController(self.view)
        self.book_controller = BookController(
            self.database,
            self.view,
            self.author_controller,
            self.genre_controller,
            self.user_controller,
            self.dialog_manager,
        )
        self.borrow_rules_controller = BorrowRulesController(self.database, self.view)

        user = None
        if self.role == "admin":
            user = User(
                "admin", "admin@gmail.com", "", "", "actif", "admin", id=5, role="admin"
            )
        elif self.role == "user":
            user = User("John Doe", "admin", "", "", "actif", "john", id=1, role="user")
        self.login_controller.login_as_user(user)
        self.book_controller.set_selected_user(user)
        self.controllers = [
            self.book_controller,
            self.author_controller,
            self.genre_controller,
            self.user_controller,
        ]

    def run(self):
        try:
            self.borrow_rules_controller.read_borrow_rules()
            for controller in self.controllers:
                controller.read_all()
        except Exception as e:
            print("Impossible de lire les tables {}".format(e))
        self.setup_ui()

        # show statusbar message
        self.book_controller.show_books_number()
        self.view.connect_signals()
        self.view.show()

    def update_toolbar_actions(self):
        """Update the state of toolbar actions based on the selection"""
        has_selection = self.view.books_table.selectionModel().hasSelection()
        is_admin = (
            self.login_controller.selected_user
            and self.login_controller.selected_user.role == "admin"
        )
        self.view.borrow_action.setEnabled(has_selection)
        self.view.restore_action.setEnabled(has_selection)
        self.view.reserve_action.setEnabled(has_selection)
        if is_admin:
            self.view.modify_action.setEnabled(has_selection)
            self.view.delete_action.setEnabled(has_selection)

    def setup_ui(self):
        if self.user_controller.users_model is not None:
            setup_table(self.view.users_table, self.user_controller.users_model)

            rows = self.user_controller.users_model.rowCount(0)

            for row in range(rows):
                id = self.user_controller.users_model.data(
                    self.user_controller.users_model.index(row, 0),
                    Qt.ItemDataRole.DisplayRole,
                )
                index = self.user_controller.users_model.index(row, 1)
                value = self.user_controller.users_model.data(
                    index, Qt.ItemDataRole.DisplayRole
                )
                self.view.user_combo_box.addItem(value, id)

        if self.author_controller.authors_model is not None:
            setup_table(self.view.authors_table, self.author_controller.authors_model)

        if self.genre_controller.genres_model is not None:
            setup_table(self.view.genres_table, self.genre_controller.genres_model)

        if self.book_controller.books_model is not None:
            setup_table(self.view.books_table, self.book_controller.books_model)

            # Connect selection change signal to enable/disable toolbar actions
            self.view.books_table.selectionModel().selectionChanged.connect(
                self.update_toolbar_actions
            )

        if (
            self.borrow_rules_controller.duree_maximale_emprunt is not None
            and self.borrow_rules_controller.penalite_retard is not None
        ):
            self.view.duree_maximale_emprunt_input.setText(
                str(self.borrow_rules_controller.duree_maximale_emprunt)
            )
            self.view.penalite_retard_input.setText(
                str(self.borrow_rules_controller.penalite_retard)
            )

    def delete_selected_item(self, name: str, index: int):
        """Delete the selected item from the table"""
        if name == "books":
            self.book_controller.delete(self.login_controller.selected_user.id)
        elif name == "genres":
            self.genre_controller.delete()
        elif name == "authors":
            self.author_controller.delete()
        elif name == "users":
            self.user_controller.delete_user()

    def add_item(self, name: str):
        if name == "books":
            self.book_controller.add(self.login_controller.selected_user.id)
        elif name == "genres":
            self.genre_controller.add()
        elif name == "authors":
            self.author_controller.add()
        elif name == "users":
            self.user_controller.add()

    def modify_selected_item(self, name: str, index: int):
        if name == "books":
            self.book_controller.modify(self.login_controller.selected_user.id)
        elif name == "genres":
            self.genre_controller.modify()
        elif name == "authors":
            self.author_controller.modify()
        elif name == "users":
            self.user_controller.modify()

    def get_column_names(self, model):
        column_names = []
        for column in range(model.columnCount(0)):
            column_name = model.headerData(
                column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            column_names.append(column_name)
        return column_names
