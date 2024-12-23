import bcrypt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.entities.user import User
from librarymanagementsystem.managers.user_manager import UserManager
from librarymanagementsystem.utils.constants import (
    USER_STATUS_ACTIF,
    USER_STATUS_EN_ATTENTE,
    USER_STATUS_INACTIF,
)
from librarymanagementsystem.utils.selection import get_selected_indexes
from librarymanagementsystem.views.login_dialog import LoginDialog
from librarymanagementsystem.views.ui import LibraryView


class LoginController:
    def __init__(self, user_manager: UserManager, view: LibraryView):
        self.view = view
        self.selected_user = None
        self.user_manager = user_manager

    def get_selected_user(self, users_model) -> dict:
        """Get the selected user from the table"""
        indexes = get_selected_indexes(self.view.users_table)
        if indexes is None:
            return (None, None)

        selected_user = (None, None)

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                users_model = users_model
                id = users_model.data(users_model.index(row, 0), role)
                nom = users_model.data(users_model.index(row, 1), role)
                selected_user = (id, nom)

                break

        return selected_user

    def change_password(self, users_model):
        dialog = LoginDialog()
        dialog.setWindowTitle("Changer le mot de passe")
        id, name = self.get_selected_user(users_model)
        print(id, name)
        if id is None:
            QMessageBox.information(
                self.view, "Utilisateur", "Veuillez sélectionner un utilisateur"
            )
            return

        dialog.populate_fields(name)
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            password = data["password"]
            print(password)
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            self.user_manager.change_password(id, hashed_password)

    def login(self, users_model):
        dialog = LoginDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            username = data["name"]
            password = data["password"]
            users_df = users_model.raw_data
            user = users_df[(users_df["nom"] == username)]
            if user.empty:
                QMessageBox.information(
                    self.view, "Utilisateur", "Utilisateur non trouvé"
                )
            else:
                hashed_password = user.iloc[0]["hash_mot_passe"]
                if not bcrypt.checkpw(
                    password.encode("utf-8"), hashed_password.encode("utf-8")
                ):
                    QMessageBox.information(
                        self.view,
                        "Utilisateur",
                        "Mot de passe incorrect",
                    )
                else:
                    status = user.iloc[0]["statut"]
                    if status == USER_STATUS_ACTIF:
                        user = User(
                            user.iloc[0]["nom"],
                            user.iloc[0]["email"],
                            user.iloc[0]["telephone"],
                            user.iloc[0]["date_naissance"],
                            user.iloc[0]["statut"],
                            user.iloc[0]["hash_mot_passe"],
                            user.iloc[0]["id_utilisateurs"],
                            user.iloc[0]["role"],
                        )
                        self.login_as_user(user)
                    elif status == USER_STATUS_INACTIF:
                        QMessageBox.information(
                            self.view,
                            "Utilisateur",
                            "Utilisateur inactif",
                        )
                    elif status == USER_STATUS_EN_ATTENTE:
                        QMessageBox.information(
                            self.view,
                            "Utilisateur",
                            "Utilisateur en attente",
                        )

    def login_as_user(self, user: User):
        """Login as a user"""
        if user is not None:
            self.view.statusBar().showMessage(f"Connecté en tant que {user.username}")
            self.view.setWindowTitle(
                f"Librairie - Connecté en tant que : {user.username}"
            )
        self.selected_user = user
        self.view.update_user_actions(user)

    def logout(self):
        """Logout the user"""
        self.view.statusBar().showMessage("Déconnecté")
        self.view.setWindowTitle("Librairie")
        self.selected_user = None
        self.view.update_user_actions(None)
        self.view.statusBar().showMessage("Déconnecté")
        self.view.setWindowTitle("Librairie")
        self.selected_user = None
        self.view.update_user_actions(None)
