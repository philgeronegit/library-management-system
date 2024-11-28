import qtawesome as qta
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QPushButton, QVBoxLayout

from librarymanagementsystem.bo.author import Author
from librarymanagementsystem.views.utils import input_factory


class AuthorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auteurs")
        self.setFixedSize(400, 200)
        self.setWindowIcon(qta.icon("fa5s.book-reader"))

        self.create_ui()

    def create_ui(self):
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.firstname_input = input_factory("Prénom :")
        self.form_layout.addRow(label, self.firstname_input)

        label, self.lastname_input = input_factory("Nom :")
        self.form_layout.addRow(label, self.lastname_input)

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
            "prenom": self.firstname_input.text().strip(),
            "nom": self.lastname_input.text().strip(),
            "id": self.author.id if hasattr(self, "author") else None,
        }

    def validate_inputs(self) -> None:
        # Validates the inputs and enables the Add button
        firstname = self.firstname_input.text().strip()
        lastname = self.lastname_input.text().strip()

        # Enable the Add button only if all fields are not empty and valid
        if firstname and lastname:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def populate_fields(self, author: Author):
        self.author = author
        self.firstname_input.setText(author.firstname)
        self.lastname_input.setText(author.lastname)
        self.validate_inputs()

        if author is not None:
            self.setWindowTitle("Modifier auteur")
            self.add_button.setText("Modifier")
