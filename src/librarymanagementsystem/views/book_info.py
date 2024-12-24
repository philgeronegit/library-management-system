import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.views.table_model import TableModel
from librarymanagementsystem.views.utils import input_factory


class BookInfo(QDialog):
    def __init__(self, authors: TableModel, genres: TableModel):
        super().__init__()
        self.setWindowTitle("Informations livre")
        self.setFixedSize(400, 400)
        self.setWindowIcon(qta.icon("fa5s.book"))

        self.authors = authors
        self.genres = genres

        self.book = None

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.title_input = input_factory("Titre :")
        self.title_input.setEnabled(False)
        self.form_layout.addRow(label, self.title_input)

        label = QLabel("Auteurs :")
        self.author_combo_box = QComboBox()
        self.authors_layout = QVBoxLayout()
        self.author_combo_box.setEnabled(False)
        self.authors_layout.addWidget(self.author_combo_box)
        self.form_layout.addRow(label, self.authors_layout)

        label = QLabel("Genre :")
        self.genre_combo_box = QComboBox()
        self.genre_combo_box.setEnabled(False)
        self.form_layout.addRow(label, self.genre_combo_box)

        label, self.publication_date_input = input_factory("Date publication :")
        self.publication_date_input.setEnabled(False)
        self.form_layout.addRow(label, self.publication_date_input)

        label, self.creation_date_input = input_factory("Date création :")
        self.creation_date_input.setEnabled(False)
        self.form_layout.addRow(label, self.creation_date_input)

        label, self.creation_by_input = input_factory("Créé par :")
        self.creation_by_input.setEnabled(False)
        self.form_layout.addRow(label, self.creation_by_input)

        label, self.modification_date_input = input_factory("Date modification :")
        self.modification_date_input.setEnabled(False)
        self.form_layout.addRow(label, self.modification_date_input)

        label, self.modification_by_input = input_factory("Modifié par :")
        self.modification_by_input.setEnabled(False)
        self.form_layout.addRow(label, self.modification_by_input)

        label, self.deletion_date_input = input_factory("Date suppression :")
        self.deletion_date_input.setEnabled(False)
        self.form_layout.addRow(label, self.deletion_date_input)

        label, self.deletion_by_input = input_factory("Supprimé par :")
        self.deletion_by_input.setEnabled(False)
        self.form_layout.addRow(label, self.deletion_by_input)

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.author_comboboxes = [self.author_combo_box]

    def populate_fields(self, book: Book):
        if book is not None:
            self.book = book
            self.title_input.setText(book.title)
            self.publication_date_input.setText(book.publication_date)
            self.creation_date_input.setText(book.creation_date)
            if book.added_by is not None:
                self.creation_by_input.setText(book.added_by.username)
            self.modification_date_input.setText(book.modification_date)
            self.deletion_date_input.setText(book.deletion_date)
            if book.modified_by is not None:
                self.modification_by_input.setText(book.modified_by.username)
            if book.deleted_by is not None:
                self.deletion_by_input.setText(book.deleted_by.username)

        author_fullname = None
        if book is not None and len(book.authors) > 0:
            author_fullname = book.authors[0].fullname
        genre = None
        if book is not None:
            genre = book.genre.name
        self.populate_combobox(
            self.author_combo_box,
            author_fullname,
            self.authors,
            self.get_author_from_model,
        )
        if book is not None and len(book.authors) > 1:
            for author in book.authors[1:]:
                self.add_author_combobox(author)
        self.populate_combobox(
            self.genre_combo_box,
            genre,
            self.genres,
            self.get_genre_from_model,
        )

    def add_author_combobox(self, author: Author = None):
        # Add a new author combobox
        author_combo_box = QComboBox()
        self.populate_combobox(
            author_combo_box,
            None,
            self.authors,
            self.get_author_from_model,
        )

        authors_layout_toolbar = QHBoxLayout()

        authors_layout_toolbar.addWidget(author_combo_box)

        self.authors_layout.addLayout(authors_layout_toolbar)

        # Ensure the layout and the parent widget update correctly
        self.authors_layout.invalidate()  # Recalculate layout
        self.authors_layout.parentWidget().adjustSize()  # Resize the dialog to fit the new content

        # Update the geometry of the parent widget if necessary
        self.authors_layout.parentWidget().updateGeometry()

        self.author_comboboxes.append(author_combo_box)

    def populate_combobox(
        self, combo_box: QComboBox, text: str, model: TableModel, fn: callable = None
    ):
        rows = model.rowCount(0)
        for row in range(rows):
            value = (
                fn(row, model)
                if fn is not None
                else model.data(model.index(row, 0), Qt.ItemDataRole.DisplayRole)
            )
            combo_box.addItem(
                value, model.data(model.index(row, 0), Qt.ItemDataRole.DisplayRole)
            )
        if text is None:
            return
        index = combo_box.findText(text)
        combo_box.setCurrentIndex(index)

    def get_genre_from_model(self, row: int, model: TableModel):
        return model.data(model.index(row, 1), Qt.ItemDataRole.DisplayRole)

    def get_author_from_model(self, row: int, model: TableModel):
        return (
            model.data(model.index(row, 2), Qt.ItemDataRole.DisplayRole)
            + " "
            + model.data(model.index(row, 1), Qt.ItemDataRole.DisplayRole)
        )
