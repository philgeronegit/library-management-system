from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMenu, QTableView


class CustomTableView(QTableView):
    def __init__(self, name, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.name = name
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        add_action = QAction("Ajouter", self)
        add_action.triggered.connect(lambda: self.controller.add_item(self.name))
        menu.addAction(add_action)
        modify_action = QAction("Modifier", self)
        modify_action.triggered.connect(lambda: self.modify_clicked(index))
        menu.addAction(modify_action)
        delete_action = QAction("Supprimer", self)
        delete_action.triggered.connect(lambda: self.delete_clicked(index))
        menu.addAction(delete_action)
        if self.name == "books":
            borrow_action = QAction("Emprunter", self)
            borrow_action.triggered.connect(lambda: self.controller.borrow_book(index))
            menu.addAction(borrow_action)
            restore_action = QAction("Restituer", self)
            restore_action.triggered.connect(
                lambda: self.controller.restore_book(index)
            )
            menu.addAction(restore_action)
        copy_action = QAction("Copier", self)
        copy_action.triggered.connect(lambda: self.copy_to_clipboard_clicked(index))
        menu.addAction(copy_action)
        menu.exec(self.viewport().mapToGlobal(position))

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

    def copy_to_clipboard_clicked(self, index):
        if not index.isValid():
            return

        data = index.data()
        clipboard = QApplication.clipboard()
        clipboard.setText(data)
