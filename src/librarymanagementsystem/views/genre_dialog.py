import qtawesome as qta
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QPushButton, QVBoxLayout

from librarymanagementsystem.entities.genre import Genre
from librarymanagementsystem.views.utils import input_factory


class GenreDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genres")
        self.setFixedSize(400, 200)
        self.setWindowIcon(qta.icon("fa5s.book-reader"))

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.name_input = input_factory("Nom :")
        self.form_layout.addRow(label, self.name_input)

        self.button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        self.add_button = QPushButton("Ok")
        self.add_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.add_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.add_button.isEnabled():
                self.accept()
            else:
                event.ignore()
        else:
            super().keyPressEvent(event)

    def get_data(self) -> dict:
        return {
            "nom": self.name_input.text().strip(),
            "id": self.genre.id if hasattr(self, "genre") else None,
        }

    def validate_inputs(self) -> None:
        # Validates the inputs and enables the Add button
        name = self.name_input.text().strip()

        # Enable the Add button only if all fields are not empty and valid
        if name:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def populate_fields(self, genre: Genre):
        self.genre = genre
        self.name_input.setText(genre.name)
        self.validate_inputs()

        if genre is not None:
            self.setWindowTitle("Modifier genre")
            self.add_button.setText("Modifier")
