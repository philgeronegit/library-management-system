from PyQt6.QtCore import Qt

from librarymanagementsystem.entities.user import User
from librarymanagementsystem.managers.user_manager import UserManager
from librarymanagementsystem.utils.selection import get_selected_indexes
from librarymanagementsystem.utils.viewport import update_viewport
from librarymanagementsystem.views.dialog_manager import DialogManager
from librarymanagementsystem.views.table_model import TableModel


class UserController:
    def __init__(self, user_manager: UserManager, view, dialog_manager: DialogManager):
        self.users_model = None
        self.user_manager = user_manager
        self.view = view
        self.dialog_manager = dialog_manager

    def read_all(self):
        df = self.user_manager.read_all()
        self.users_model = TableModel(df)
        print(f"Empty {df.empty}")
        update_viewport(self.view.users_table, self.users_model)

    def add(self):
        """Add a new user to the list"""
        new_user = self.dialog_manager.add_user()
        if new_user is None:
            return

        self.user_manager.insert(new_user)
        self.read_all()

    def modify(self):
        """Modify a user from the list"""
        user = self.get_selected_user()
        if user is None:
            return

        existing_user = self.dialog_manager.modify_user(user)
        if existing_user is None:
            return
        self.user_manager.modify(existing_user)
        self.read_all()

    def delete(self):
        """Delete a user from the list"""
        user = self.get_selected_user()
        if user is None:
            return

        to_delete = self.dialog_manager.delete_user(user)
        if not to_delete:
            return
        self.user_manager.delete(user.id)
        self.read_all()

    def find_user(self, id: int) -> User | None:
        """Find a user by id"""
        user_df = self.users_model.raw_data[
            self.users_model.raw_data["id_utilisateurs"] == id
        ]
        if user_df.empty:
            return None

        name = user_df["nom"].values[0]
        email = user_df["email"].values[0]
        phone = user_df["telephone"].values[0]
        birthday = user_df["date_naissance"].values[0]
        status = user_df["statut"].values[0]
        password = user_df["hash_mot_passe"].values[0]
        user = User(
            name,
            email,
            phone,
            birthday,
            status,
            password,
            id,
        )
        return user

    def get_selected_user(self) -> dict:
        """Get the selected user from the table"""
        indexes = get_selected_indexes(self.view.users_table)
        if indexes is None:
            return None

        selected_user = None

        for index in indexes:
            if index.isValid():
                row = index.row()
                role = Qt.ItemDataRole.DisplayRole

                users_model = self.users_model
                id = users_model.data(users_model.index(row, 0), role)
                name = users_model.data(users_model.index(row, 1), role)
                password = users_model.data(users_model.index(row, 2), role)
                email = users_model.data(users_model.index(row, 3), role)
                phone = users_model.data(users_model.index(row, 4), role)
                birthday = users_model.data(users_model.index(row, 5), role)
                status = users_model.data(users_model.index(row, 6), role)
                role = users_model.data(users_model.index(row, 7), role)
                selected_user = User(
                    name, email, phone, birthday, status, password, id=id, role=role
                )
                break

        return selected_user
