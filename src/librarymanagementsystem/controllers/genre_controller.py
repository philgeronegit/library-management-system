from PyQt6.QtCore import Qt

from librarymanagementsystem.entities.genre import Genre
from librarymanagementsystem.managers.genre_manager import GenreManager
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.utils.selection import get_selected_indexes
from librarymanagementsystem.utils.viewport import update_viewport
from librarymanagementsystem.views.table_model import TableModel


class GenreController:
    def __init__(self, database: Database, view, dialog_manager):
        self.genres_model = None
        self.genre_manager = GenreManager(database)
        self.view = view
        self.dialog_manager = dialog_manager

    def read_all(self):
        df = self.genre_manager.read_all()
        self.genres_model = TableModel(df)
        self.update_viewport_genres()

    def add(self):
        """Add a new genre to the list"""
        new_genre = self.dialog_manager.add_genre()
        if new_genre is None:
            return
        self.genre_manager.insert(new_genre)
        self.read_all()

    def modify(self):
        """Modify a author from the list"""
        genre = self.get_selected_genre()
        if genre is None:
            return

        existing_genre = self.dialog_manager.modify_genre(genre)
        if existing_genre is None:
            return
        self.genre_manager.modify(existing_genre)
        self.read_all()

    def delete(self):
        """Delete a genre from the list"""
        genre = self.get_selected_genre()
        if genre is None:
            return

        to_delete = self.dialog_manager.delete_genre(genre)
        if not to_delete:
            return
        self.genre_manager.delete(genre.id)
        self.read_all()

    def find_genre(self, id: int) -> Genre | None:
        """Find a genre by id"""
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

    def get_selected_genre(self) -> dict:
        """Get the selected genre from the table"""
        indexes = get_selected_indexes(self.view.genres_table)
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

    def update_viewport_genres(self):
        update_viewport(self.view.genres_table, self.genres_model)
