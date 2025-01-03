import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from librarymanagementsystem.views.utils import input_factory


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 200)
        self.setWindowIcon(qta.icon("fa5s.user"))

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        label, self.name_input = input_factory("Nom :")
        self.form_layout.addRow(label, self.name_input)

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
            "name": self.name_input.text().strip(),
            "password": self.password_input.text().strip(),
        }

    def populate_fields(self, user_name: str):
        self.name_input.setText(user_name)
        self.name_input.setEnabled(False)
