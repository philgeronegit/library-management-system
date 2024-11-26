from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QTableView


class CustomTableView(QTableView):
    def __init__(self, name, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.name = name

        self.create_ui()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def create_ui(self):
        self.menu = QMenu()
        self.add_action = QAction("Ajouter", self)
        self.add_action.setEnabled(False)
        self.add_action.triggered.connect(lambda: self.controller.add_item(self.name))
        self.menu.addAction(self.add_action)
        self.modify_action = QAction("Modifier", self)
        self.modify_action.setEnabled(False)

        self.menu.addAction(self.modify_action)
        self.delete_action = QAction("Supprimer", self)
        self.delete_action.setEnabled(False)
        self.menu.addAction(self.delete_action)
        if self.name == "books":
            borrow_action = QAction("Emprunter", self)
            borrow_action.triggered.connect(self.controller.borrow_book)
            self.menu.addAction(borrow_action)
            restore_action = QAction("Restituer", self)
            restore_action.triggered.connect(self.controller.restore_book)
            self.menu.addAction(restore_action)

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
        self.controller.delete_selected_item(self.name, index)

    def modify_clicked(self, index):
        index = self.get_index_data(index)
        self.controller.modify_selected_item(self.name, index)
