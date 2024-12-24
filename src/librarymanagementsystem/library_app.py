from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView

from librarymanagementsystem.controllers.author_controller import AuthorController
from librarymanagementsystem.controllers.book_controller import BookController
from librarymanagementsystem.controllers.borrow_rules_controller import (
    BorrowRulesController,
)
from librarymanagementsystem.controllers.genre_controller import GenreController
from librarymanagementsystem.controllers.login_controller import LoginController
from librarymanagementsystem.controllers.user_controller import UserController
from librarymanagementsystem.entities.user import User
from librarymanagementsystem.managers.user_manager import UserManager
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.utils.constants import (
    USER_ROLE_ADMIN,
    USER_ROLE_USER,
    USER_STATUS_ACTIF,
)
from librarymanagementsystem.utils.selection import get_column_index_by_name
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
        user_manager = UserManager(self.database)
        self.user_controller = UserController(
            user_manager, self.view, self.dialog_manager
        )
        self.login_controller = LoginController(user_manager, self.view)
        self.book_controller = BookController(
            self.database,
            self.view,
            self.author_controller,
            self.genre_controller,
            self.user_controller,
            self.login_controller,
            self.dialog_manager,
        )
        self.borrow_rules_controller = BorrowRulesController(self.database, self.view)

        user = None
        if self.role == USER_ROLE_ADMIN:
            user = User(
                "admin",
                "admin@gmail.com",
                "+336",
                "1990-01-01",
                USER_STATUS_ACTIF,
                "admin",
                id=5,
                role=USER_ROLE_ADMIN,
            )
        elif self.role == "user":
            user = User(
                "John Doe",
                "john.doe@gmail.com",
                "+336",
                "1990-01-01",
                USER_STATUS_ACTIF,
                "john",
                id=1,
                role=USER_ROLE_USER,
            )
        self.login_controller.login_as_user(user)
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
            and self.login_controller.selected_user.role == USER_ROLE_ADMIN
        )
        self.view.borrow_action.setEnabled(has_selection)
        self.view.restore_action.setEnabled(has_selection)
        self.view.reserve_action.setEnabled(has_selection)
        if is_admin:
            self.view.modify_action.setEnabled(has_selection)
            self.view.delete_action.setEnabled(has_selection)

    def setup_table(self, table_view, model, hide_columns=[]):
        table_view.setModel(model)
        table_view.resizeColumnsToContents()
        table_view.setSortingEnabled(True)
        table_view.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        table_view.setColumnHidden(0, True)
        for column in hide_columns:
            index = get_column_index_by_name(model, column)
            table_view.setColumnHidden(index, True)
        table_view.verticalHeader().setVisible(False)
        table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def setup_ui(self):
        if self.user_controller.users_model is not None:
            self.setup_table(
                self.view.users_table,
                self.user_controller.users_model,
                ["hash_mot_passe", "id_reservations"],
            )

            rows = self.user_controller.users_model.rowCount(0)

            for row in range(rows):
                id = self.user_controller.users_model.data(
                    self.user_controller.users_model.index(row, 0),
                    Qt.ItemDataRole.DisplayRole,
                )
                name = self.user_controller.users_model.data(
                    self.user_controller.users_model.index(row, 1),
                    Qt.ItemDataRole.DisplayRole,
                )
                role = get_column_index_by_name(
                    self.user_controller.users_model, "role"
                )
                if role != USER_ROLE_ADMIN:
                    self.view.user_combo_box.addItem(name, id)

        if self.author_controller.authors_model is not None:
            self.setup_table(
                self.view.authors_table, self.author_controller.authors_model
            )

        if self.genre_controller.genres_model is not None:
            self.setup_table(self.view.genres_table, self.genre_controller.genres_model)

        if self.book_controller.books_model is not None:
            self.setup_table(self.view.books_table, self.book_controller.books_model)

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
            self.user_controller.delete()

    def add_item(self, name: str):
        if name == "books":
            self.book_controller.add(self.login_controller.selected_user.id)
        elif name == "genres":
            self.genre_controller.add()
        elif name == "authors":
            self.author_controller.add()
        elif name == "users":
            self.user_controller.add()

    def show_selected_item(self, name: str, index: int):
        if name == "books":
            self.book_controller.show_book_info()

    def modify_selected_item(self, name: str, index: int):
        if name == "books":
            self.book_controller.modify(self.login_controller.selected_user.id)
        elif name == "genres":
            self.genre_controller.modify()
        elif name == "authors":
            self.author_controller.modify()
        elif name == "users":
            self.user_controller.modify()

    def change_password(self):
        self.login_controller.change_password(self.user_controller.users_model)
        self.user_controller.read_all()

    def get_column_names(self, model):
        column_names = []
        for column in range(model.columnCount(0)):
            column_name = model.headerData(
                column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole
            )
            column_names.append(column_name)
        return column_names
