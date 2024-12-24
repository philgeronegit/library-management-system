from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QTableView


class CustomTableView(QTableView):
    def __init__(self, name: str, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.name = name

        self.create_ui()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def create_ui(self):
        self.menu = QMenu()
        self.add_action = QAction("Ajouter", self)
        self.add_action.setEnabled(False)
        self.add_action.triggered.connect(lambda: self.app.add_item(self.name))
        self.menu.addAction(self.add_action)
        self.modify_action = QAction("Modifier", self)
        self.modify_action.setEnabled(False)

        self.menu.addAction(self.modify_action)
        self.delete_action = QAction("Supprimer", self)
        self.delete_action.setEnabled(False)
        self.menu.addAction(self.delete_action)

    def connect_signals(self):
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.doubleClicked.connect(self.on_double_click)

    def show_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return

        self.modify_action.triggered.disconnect()
        self.modify_action.triggered.connect(lambda: self.modify_clicked(index))
        self.delete_action.triggered.disconnect()
        self.delete_action.triggered.connect(lambda: self.delete_clicked(index))
        self.menu.exec(self.viewport().mapToGlobal(position))

    def get_index_data(self, index):
        if not index.isValid():
            return None

        return self.model().index(index.row(), 0).data()

    def delete_clicked(self, index):
        index = self.get_index_data(index)
        self.app.delete_selected_item(self.name, index)

    def modify_clicked(self, index):
        index = self.get_index_data(index)
        self.app.modify_selected_item(self.name, index)

    def on_double_click(self, index):
        if not index.isValid():
            return

        index = self.get_index_data(index)
        self.app.show_selected_item(self.name, index)


class CustomTableViewBook(CustomTableView):
    def __init__(self, name, app, parent=None):
        super().__init__(name, app, parent)

    def create_ui(self):
        super().create_ui()
        self.borrow_action = QAction("Emprunter", self)
        self.borrow_action.setEnabled(False)
        self.menu.addAction(self.borrow_action)

        self.restore_action = QAction("Restituer", self)
        self.restore_action.setEnabled(False)
        self.menu.addAction(self.restore_action)

    def connect_signals(self):
        super().connect_signals()
        self.borrow_action.triggered.connect(self.app.book_controller.borrow_book)
        self.restore_action.triggered.connect(self.app.book_controller.restore_book)


class CustomTableViewUser(CustomTableView):
    def __init__(self, name, app, parent=None):
        super().__init__(name, app, parent)

    def create_ui(self):
        super().create_ui()
        self.change_password_action = QAction("Changer mot de passe", self)
        self.menu.addAction(self.change_password_action)

    def connect_signals(self):
        super().connect_signals()
        self.change_password_action.triggered.connect(self.app.change_password)
