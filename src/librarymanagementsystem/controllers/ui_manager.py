from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView


class UIManager:
    def __init__(self, view):
        self.view = view

    def setup_users_table(self, users_model):
        self.view.users_table.setModel(users_model)
        self.view.users_table.resizeColumnsToContents()
        self.view.users_table.setSortingEnabled(True)
        self.view.users_table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.view.users_table.setColumnHidden(0, True)
        self.view.users_table.verticalHeader().setVisible(False)
        self.view.users_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

    def setup_authors_table(self, authors_model):
        self.view.authors_table.setModel(authors_model)
        self.view.authors_table.resizeColumnsToContents()
        self.view.authors_table.setSortingEnabled(True)
        self.view.authors_table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.view.authors_table.setColumnHidden(0, True)
        self.view.authors_table.verticalHeader().setVisible(False)
        self.view.authors_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

    def setup_genres_table(self, genres_model):
        self.view.genres_table.setModel(genres_model)
        self.view.genres_table.resizeColumnsToContents()
        self.view.genres_table.setSortingEnabled(True)
        self.view.genres_table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.view.genres_table.setColumnHidden(0, True)
        self.view.genres_table.verticalHeader().setVisible(False)
        self.view.genres_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

    def setup_books_table(self, books_model):
        self.view.books_table.setModel(books_model)
        self.view.books_table.resizeColumnsToContents()
        self.view.books_table.setSortingEnabled(True)
        self.view.books_table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.view.books_table.setMouseTracking(True)
        self.view.books_table.setColumnHidden(0, True)
        self.view.books_table.verticalHeader().setVisible(False)
        self.view.books_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
