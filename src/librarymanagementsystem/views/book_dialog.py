import qtawesome as qta
from dateutil.parser import parse
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from librarymanagementsystem.models.author import Author
from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.table_model import TableModel
from librarymanagementsystem.views.utils import input_factory


class BookDialog(QDialog):
    def __init__(self, authors: TableModel, genres: TableModel):
        super().__init__()
        self.setWindowTitle("Ajouter livre")
        self.setFixedSize(400, 400)
        self.setWindowIcon(qta.icon("fa5s.book"))

        self.authors = authors
        self.genres = genres

        self.book = None

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.titre_input = input_factory("Titre :")
        self.form_layout.addRow(label, self.titre_input)

        label = QLabel("Auteur :")
        self.author_combo_box = QComboBox()
        self.authors_layout = QVBoxLayout()
        authors_layout_toolbar = QHBoxLayout()

        # Add a + icon button using qt_awesome to add another phone number
        add_author_button = QPushButton()
        add_author_button.setIcon(qta.icon("fa5s.plus"))
        add_author_button.clicked.connect(lambda: self.add_author_combobox())

        authors_layout_toolbar.addWidget(self.author_combo_box)
        authors_layout_toolbar.addWidget(add_author_button)
        self.authors_layout.addLayout(authors_layout_toolbar)
        self.form_layout.addRow(label, self.authors_layout)

        label = QLabel("Genre :")
        self.genre_combo_box = QComboBox()
        self.form_layout.addRow(label, self.genre_combo_box)

        label, self.date_publication_input = input_factory("Date publication :")
        self.form_layout.addRow(label, self.date_publication_input)

        self.button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        self.add_button = QPushButton("Ajouter")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.add_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        # Connect textChanged signals to the validation method
        self.date_publication_input.textChanged.connect(self.validate_inputs)

        self.author_comboboxes = [self.author_combo_box]

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.add_button.isEnabled():
                self.accept()
            else:
                event.ignore()
        else:
            super().keyPressEvent(event)

    def del_author_combobox(self, author_id: int, layout: QVBoxLayout):
        # Delete a phone input field
        for author_combobox in self.author_comboboxes:
            if author_combobox.currentData() == author_id:
                self.author_comboboxes.remove(author_combobox)
                break

        # Remove and delete each widget in the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Finally, delete the layout itself
        layout.deleteLater()

        # Update the layout to reflect the changes
        self.authors_layout.update()
        self.authors_layout.parentWidget().updateGeometry()

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

        # Add a + icon button using qt_awesome to add another phone number
        add_author_button = QPushButton()
        add_author_button.setIcon(qta.icon("fa5s.plus"))
        add_author_button.clicked.connect(lambda: self.add_author_combobox())

        del_author_button = QPushButton()
        del_author_button.setIcon(qta.icon("fa5s.minus"))
        # Add the author id to know which one to delete
        del_author_button.clicked.connect(
            lambda: self.del_author_combobox(
                author_combo_box.currentData(), authors_layout_toolbar
            )
        )

        authors_layout_toolbar.addWidget(author_combo_box)
        authors_layout_toolbar.addWidget(add_author_button)
        authors_layout_toolbar.addWidget(del_author_button)

        self.authors_layout.addLayout(authors_layout_toolbar)

        # Ensure the layout and the parent widget update correctly
        self.authors_layout.invalidate()  # Recalculate layout
        self.authors_layout.parentWidget().adjustSize()  # Resize the dialog to fit the new content

        # Update the geometry of the parent widget if necessary
        self.authors_layout.parentWidget().updateGeometry()

        self.author_comboboxes.append(author_combo_box)

    def get_data(self) -> dict:
        authord_ids = []
        for author_combobox in self.author_comboboxes:
            # check if not already added
            if author_combobox.currentData() not in authord_ids:
                authord_ids.append(int(author_combobox.currentData()))
        data = {
            "id": self.book.id if self.book is not None else None,
            "titre": self.titre_input.text().strip(),
            "auteur_ids": authord_ids,
            "genre": self.genre_combo_box.currentText().strip(),
            "genre_id": self.genre_combo_box.currentData(),
            "date_publication": self.date_publication_input.text().strip(),
        }
        return data

    def is_valid_date(self, date_string: str) -> bool:
        try:
            parse(date_string)
            return True
        except ValueError:
            return False

    def validate_inputs(self) -> None:
        # Validates the inputs and enables the Add button
        titre = self.titre_input.text().strip()
        auteur = self.author_combo_box.currentText().strip()
        genre = self.genre_combo_box.currentText().strip()
        date_publication = self.date_publication_input.text().strip()

        date_valid = self.is_valid_date(date_publication)

        # Enable the Add button only if all fields are not empty and valid
        if titre and auteur and genre and date_valid:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def get_property_or_none(self, instance, property) -> str | None:
        return getattr(instance, property) if instance is not None else None

    def populate_fields(self, book: Book):
        if book is not None:
            self.book = book
            self.titre_input.setText(book.titre)
            self.date_publication_input.setText(book.date_publication)

        author_fullname = None
        if book is not None and len(book.auteurs) > 0:
            author_fullname = book.auteurs[0].fullname
        genre = None
        if book is not None:
            genre = book.genre.name
        self.populate_combobox(
            self.author_combo_box,
            author_fullname,
            self.authors,
            self.get_author_from_model,
        )
        if book is not None and len(book.auteurs) > 1:
            for author in book.auteurs[1:]:
                self.add_author_combobox(author)
        self.populate_combobox(
            self.genre_combo_box,
            genre,
            self.genres,
            self.get_genre_from_model,
        )
        self.validate_inputs()

        self.setWindowTitle("Modifier livre")
        self.add_button.setText("Modifier")

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
