import qtawesome as qta
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from librarymanagementsystem.entities.user import User
from librarymanagementsystem.utils.constants import (
    USER_ROLE_ADMIN,
    USER_ROLE_USER,
    USER_STATUS_ACTIF,
    USER_STATUS_EN_ATTENTE,
    USER_STATUS_INACTIF,
)
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

        label, self.email_input = input_factory("Email :")
        self.form_layout.addRow(label, self.email_input)

        label, self.phone_input = input_factory("Téléphone :")
        self.form_layout.addRow(label, self.phone_input)

        label, self.birth_date_input = input_factory("Date naissance :")
        self.birth_date_input.setInputMask("0000-00-00")
        self.form_layout.addRow(label, self.birth_date_input)

        label = QLabel("Statut :")
        self.status_combo_box = QComboBox()
        self.form_layout.addRow(label, self.status_combo_box)
        self.status_combo_box.addItem(USER_STATUS_ACTIF)
        self.status_combo_box.addItem(USER_STATUS_INACTIF)
        self.status_combo_box.addItem(USER_STATUS_EN_ATTENTE)

        label = QLabel("Role :")
        self.role_combo_box = QComboBox()
        self.form_layout.addRow(label, self.role_combo_box)
        self.role_combo_box.addItem(USER_ROLE_USER)
        self.role_combo_box.addItem(USER_ROLE_ADMIN)

        label, self.password_input = input_factory("Mot de passe ")
        self.password_label = label
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
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "birthday": self.birth_date_input.text().strip(),
            "status": self.status_combo_box.currentText(),
            "role": self.role_combo_box.currentText(),
            "password": self.password_input.text().strip(),
            "id": self.user.id if hasattr(self, "user") else None,
        }

    def validate_inputs(self) -> None:
        # Validates the inputs and enables the Add button
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        is_email = "@" in email and "." in email
        phone = self.phone_input.text().strip()
        is_phone = phone.startswith("+") and len(phone) >= 3
        password = self.password_input.text().strip()

        # Enable the Add button only if all fields are not empty and valid
        if name and is_email and is_phone and password and len(password) >= 3:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def populate_fields(self, user: User):
        self.user = user
        self.name_input.setText(user.username)
        self.email_input.setText(user.email)
        self.phone_input.setText(user.phone)
        self.birth_date_input.setText(user.birthday)
        self.status_combo_box.setCurrentText(user.status)
        self.role_combo_box.setCurrentText(user.role)
        self.password_input.setText(user.password)
        self.validate_inputs()

        if user is not None:
            self.setWindowTitle("Modifier utilisateur")
            self.add_button.setText("Modifier")
            self.password_label.setVisible(False)
            self.password_input.setVisible(False)
            self.setWindowTitle("Modifier utilisateur")
            self.add_button.setText("Modifier")
            self.password_label.setVisible(False)
            self.password_input.setVisible(False)
