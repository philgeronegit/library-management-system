from PyQt6.QtCore import Qt

from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.managers.author_manager import AuthorManager
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.utils.selection import get_selected_indexes
from librarymanagementsystem.utils.viewport import update_viewport
from librarymanagementsystem.views.table_model import TableModel


class AuthorController:
    def __init__(self, database: Database, view, dialog_manager):
        self.authors_model = None
        self.author_manager = AuthorManager(database)
        self.view = view
        self.dialog_manager = dialog_manager

    def read_all(self):
        df = self.author_manager.read_all()
        self.authors_model = TableModel(df)
        self.update_viewport_authors()

    def add(self):
        """Add a new author to the list"""
        new_author = self.dialog_manager.add_author()
        if new_author is None:
            return
        self.author_manager.insert(new_author)
        self.read_all()

    def modify(self):
        """Modify a author from the list"""
        author = self.get_selected_author()
        if author is None:
            return

        existing_author = self.dialog_manager.modify_author(author)
        if existing_author is None:
            return
        self.author_manager.modify(existing_author)
        self.read_all()

    def delete(self):
        """Delete a author from the list"""
        author = self.get_selected_author()
        if author is None:
            return

        to_delete = self.dialog_manager.delete_author(author)
        if not to_delete:
            return
        self.author_manager.delete(author.id)
        self.read_all()

    def find_author(self, id: int) -> Author | None:
        """Find an author by id"""
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

    def get_selected_author(self) -> dict:
        """Get the selected author from the table"""
        indexes = get_selected_indexes(self.view.authors_table)
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

    def update_viewport_authors(self):
        update_viewport(self.view.authors_table, self.authors_model)
