from PyQt6.QtWidgets import QDialog, QMessageBox

from librarymanagementsystem.entities.user import User
from librarymanagementsystem.views.login_dialog import LoginDialog


class LoginController:
    def __init__(self, view):
        self.view = view
        self.selected_user = None

    def login(self):
        dialog = LoginDialog()
        response = dialog.exec()
        if response == QDialog.Accepted:
            data = dialog.get_data()
            username = data["nom"]
            password = data["hash_mot_passe"]
            if (username == "admin") and (password == "admin"):
                user = User(username, "admin", "", "", "actif", password, role="admin")
                self.login_as_user(user)
            else:
                users_df = self.user_controller.users_model.raw_data
                user = users_df[(users_df["nom"] == username)]
                if user.empty:
                    QMessageBox.information(
                        self.view, "Utilisateur", "Utilisateur non trouvé"
                    )
                else:
                    user_password = user.iloc[0]["hash_mot_passe"]
                    if user_password != user_password:
                        QMessageBox.information(
                            self.view,
                            "Utilisateur",
                            "Mot de passe incorrect",
                        )
                    else:
                        status = user.iloc[0]["statut"]
                        if status == "actif":
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
                        elif status == "inactif":
                            QMessageBox.information(
                                self.view,
                                "Utilisateur",
                                "Utilisateur inactif",
                            )
                        elif status == "en-attente":
                            QMessageBox.information(
                                self.view,
                                "Utilisateur",
                                "Utilisateur en attente",
                            )

    def login_as_user(self, user: User):
        """Login as a user"""
        if user is None:
            return

        self.view.statusBar().showMessage(f"Connecté en tant que {user.username}")
        self.view.setWindowTitle(f"Librairie - Connecté en tant que : {user.username}")
        self.selected_user = user
        self.view.update_user_actions(user)

    def logout(self):
        """Logout the user"""
        self.view.statusBar().showMessage("Déconnecté")
        self.view.setWindowTitle("Librairie")
        self.selected_user = None
        self.view.update_user_actions(None)
