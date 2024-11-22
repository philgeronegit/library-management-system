import qtawesome as qta
from dateutil.parser import parse
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

from librarymanagementsystem.models.book import Book
from librarymanagementsystem.models.table_model import TableModel
from librarymanagementsystem.views.utils import input_factory


class BookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter livre")
        self.setFixedSize(400, 400)
        self.setWindowIcon(qta.icon("fa5s.book"))

        self.book = None

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.titre_input = input_factory("Titre :")
        self.form_layout.addRow(label, self.titre_input)

        label = QLabel("Auteur :")
        self.auteur_combo_box = QComboBox()
        self.form_layout.addRow(label, self.auteur_combo_box)

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

    def get_data(self) -> dict:
        return {
            "id": self.book.id if self.book is not None else None,
            "titre": self.titre_input.text().strip(),
            "auteur": self.auteur_combo_box.currentText().strip(),
            "auteur_id": self.auteur_combo_box.currentData(),
            "genre": self.genre_combo_box.currentText().strip(),
            "genre_id": self.genre_combo_box.currentData(),
            "date_publication": self.date_publication_input.text().strip(),
        }

    def is_valid_date(self, date_string: str) -> bool:
        try:
            parse(date_string)
            return True
        except ValueError:
            return False

    def validate_inputs(self) -> None:
        # Validates the inputs and enables the Add button
        titre = self.titre_input.text().strip()
        auteur = self.auteur_combo_box.currentText().strip()
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

    def populate_fields(self, book: Book, authors: TableModel, genres: TableModel):
        if book is not None:
            self.book = book
            self.titre_input.setText(book.titre)
            self.date_publication_input.setText(book.date_publication)

        author_fullname = None
        if book is not None:
            author_fullname = book.auteur.fullname
        genre = None
        if book is not None:
            genre = book.genre.name
        self.populate_combobox(
            self.auteur_combo_box,
            author_fullname,
            authors,
            self.get_author_from_model,
        )
        self.populate_combobox(
            self.genre_combo_box,
            genre,
            genres,
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
