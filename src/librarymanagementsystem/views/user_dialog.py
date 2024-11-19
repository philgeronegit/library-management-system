import qtawesome as qta
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from librarymanagementsystem.models.user import User
from librarymanagementsystem.views.utils import input_factory


class UserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utilisateur")
        self.setFixedSize(400, 200)
        self.setWindowIcon(qta.icon("fa5s.user"))

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.name_input = input_factory("Nom :")
        self.form_layout.addRow(label, self.name_input)

        label, self.contact_input = input_factory("Contact :")
        self.form_layout.addRow(label, self.contact_input)

        label, self.status_input = input_factory("Statut :")
        self.form_layout.addRow(label, self.status_input)

        label, self.password_input = input_factory("Mot de passe ")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.form_layout.addRow(label, self.password_input)

        self.button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        self.add_button = QPushButton("Ok")
        self.add_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.add_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def get_data(self) -> dict:
        return {
            "nom": self.name_input.text().strip(),
            "contact": self.contact_input.text().strip(),
            "statut": self.status_input.text().strip(),
            "mot_passe": self.password_input.text().strip(),
            "id": self.user.id if hasattr(self, "user") else None,
        }

    def validate_inputs(self) -> None:
        # Validates the inputs and enables the Add button
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        status = self.status_input.text().strip()
        password = self.password_input.text().strip()

        # Enable the Add button only if all fields are not empty and valid
        if name and password and contact and status and len(password) >= 3:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def populate_fields(self, user: User):
        self.user = user
        self.name_input.setText(user.username)
        self.contact_input.setText(user.contact)
        self.status_input.setText(user.status)
        self.password_input.setText(user.password)
        self.validate_inputs()
        self.setWindowTitle("Modifier utilisateur")
        self.add_button.setText("Modifier")
