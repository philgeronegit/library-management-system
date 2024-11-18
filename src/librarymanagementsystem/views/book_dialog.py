import qtawesome as qta
from dateutil.parser import parse
from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QPushButton, QVBoxLayout

from librarymanagementsystem.models.book import Book
from librarymanagementsystem.views.utils import input_factory


class BookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter livre")
        self.setFixedSize(400, 400)
        self.setWindowIcon(qta.icon("fa5s.book"))

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.titre_input = input_factory("Titre :")
        self.form_layout.addRow(label, self.titre_input)

        label, self.auteur_input = input_factory("Auteur ")
        self.form_layout.addRow(label, self.auteur_input)

        label, self.genre_input = input_factory("Genre :")
        self.form_layout.addRow(label, self.genre_input)

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
            "titre": self.titre_input.text().strip(),
            "auteur": self.auteur_input.text().strip(),
            "genre": self.genre_input.text().strip(),
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
        auteur = self.auteur_input.text().strip()
        genre = self.genre_input.text().strip()
        date_publication = self.date_publication_input.text().strip()

        date_valid = self.is_valid_date(date_publication)

        # Enable the Add button only if all fields are not empty and valid
        if titre and auteur and genre and date_valid:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def populate_fields(self, book: Book):
        self.titre_input.setText(book.titre)
        self.auteur_input.setText(book.auteur)
        self.genre_input.setText(book.genre)
        self.date_publication_input.setText(book.date_publication)
        self.validate_inputs()
        self.setWindowTitle("Modifier livre")
        self.add_button.setText("Modifier")
