import sys

import qtawesome as qta
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from librarymanagementsystem.models.user import User
from librarymanagementsystem.views.components.clearable_line_edit import (
    ClearableLineEdit,
)
from librarymanagementsystem.views.components.custom_table_view import CustomTableView
from librarymanagementsystem.views.constants import LIGHT_GREEN_COLOR
from librarymanagementsystem.views.utils import input_factory


class LibraryView(QMainWindow):
    def __init__(self, controller=None):
        super().__init__()
        icon = qta.icon("fa5s.book")
        self.setWindowIcon(icon)
        self.setWindowTitle("Librairie")

        self.is_ready = False
        self.controller = controller
        self.create_ui()

        # Set minimum width and make the window resizable
        self.setMinimumWidth(1024)
        self.setMinimumHeight(768)  # Optional: Set a minimum height if needed
        self.resize(1024, 768)  # Set the initial size

        # Center the window on the screen
        self.center()

    def center(self):
        # Center the window on the screen using QScreen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def create_ui(self):
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Fichier")
        self.exit_action = self.file_menu.addAction("Quitter")
        self.exit_action.triggered.connect(self.close)
        self.user_menu = self.menu.addMenu("Utilisateur")
        self.login_action = self.user_menu.addAction("Login")
        self.login_action.triggered.connect(self.login)
        self.logout_action = self.user_menu.addAction("Logout")
        self.logout_action.triggered.connect(self.logout)
        self.logout_action.setEnabled(False)

        self.centralWidget = QWidget()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.centralWidget.setLayout(self.layout)

        self.tab = QTabWidget()
        livres_tab = QWidget()
        self.livres_tab_layout = QVBoxLayout()
        self.livres_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        livres_tab.setLayout(self.livres_tab_layout)
        self.tab.addTab(livres_tab, "Livres")

        utilisateurs_tab = QWidget()
        self.utilisateurs_tab_layout = QVBoxLayout()
        self.utilisateurs_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        utilisateurs_tab.setLayout(self.utilisateurs_tab_layout)
        self.tab.addTab(utilisateurs_tab, "Utilisateurs")

        regles_prets_tab = QWidget()
        self.regles_prets_tab_layout = QVBoxLayout()
        self.regles_prets_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout = QFormLayout()
        self.regles_prets_tab_layout.addLayout(form_layout)
        label, self.duree_maximale_emprunt_input = input_factory(
            "Durée maximale emprunt :"
        )
        form_layout.addRow(label, self.duree_maximale_emprunt_input)
        label, self.penalite_retard_input = input_factory("Pénalité de retard :")
        form_layout.addRow(label, self.penalite_retard_input)
        self.save_regles_prets_button = QPushButton("Sauver")
        self.save_regles_prets_button.clicked.connect(
            self.controller.save_regles_prets_clicked
        )
        self.regles_prets_tab_layout.addWidget(self.save_regles_prets_button)

        regles_prets_tab.setLayout(self.regles_prets_tab_layout)
        self.tab.addTab(regles_prets_tab, "Règles de prêts")

        self.layout.addWidget(self.tab)

        self.search_input = ClearableLineEdit()
        self.search_input.setPlaceholderText("Recherche de livres, auteurs, genres.")
        self.livres_tab_layout.addWidget(self.search_input)

        self.filter_layout = QHBoxLayout()
        self.filter_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.all_books_radio = QRadioButton("Tous les livres")
        self.all_books_radio.setProperty("type", "all")
        self.all_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.all_books_radio.setChecked(True)
        self.available_books_radio = QRadioButton("Livres disponibles")
        self.available_books_radio.setProperty("type", "available")
        self.available_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.borrowed_books_radio = QRadioButton("Livres empruntés")
        self.borrowed_books_radio.setProperty("type", "borrowed")
        self.borrowed_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.late_books_radio = QRadioButton("Retours en retard")
        self.setProperty("type", "late")
        self.late_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.user_combo_box = QComboBox()
        self.user_combo_box.addItem("Tous")
        self.user_combo_box.addItem("Admin")
        self.is_ready = True

        self.filter_layout.addWidget(self.all_books_radio)
        self.filter_layout.addWidget(self.available_books_radio)
        self.filter_layout.addWidget(self.borrowed_books_radio)
        self.filter_layout.addWidget(self.late_books_radio)
        label = QLabel("Utilisateurs")
        self.filter_layout.addWidget(label)
        self.filter_layout.addWidget(self.user_combo_box)
        self.livres_tab_layout.addLayout(self.filter_layout)

        self.books_table = CustomTableView("books", self.controller)
        self.livres_tab_layout.addWidget(self.books_table)

        self.users_table = CustomTableView("users", self.controller)
        self.utilisateurs_tab_layout.addWidget(self.users_table)

        self.setCentralWidget(self.centralWidget)

        self.create_toolbar()

        # Create a QTimer for debouncing
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

        # Connect the textChanged signal to restart the timer
        self.search_input.textChanged.connect(self.restart_search_timer)

    def handle_radio_button_toggled(self):
        if not self.is_ready:
            return

        rbtn = self.sender()
        self.controller.filter_change(rbtn.property("type"))

    def closeEvent(self, event):
        event.accept()
        sys.exit()

    def login(self):
        self.controller.login()

    def logout(self):
        self.controller.logout()

    def update_user_actions(self, user: User = None):
        if user is None:
            self.login_action.setEnabled(True)
            self.logout_action.setEnabled(False)
            return

        self.login_action.setEnabled(False)
        self.logout_action.setEnabled(True)

        if user.role == "admin":
            self.add_action.setEnabled(True)
            self.modify_action.setEnabled(True)
            self.delete_action.setEnabled(True)
            self.borrow_action.setEnabled(False)
            self.restore_action.setEnabled(False)
            self.reserve_action.setEnabled(False)
        else:
            self.add_action.setEnabled(False)
            self.modify_action.setEnabled(False)
            self.delete_action.setEnabled(False)
            self.borrow_action.setEnabled(True)
            self.restore_action.setEnabled(True)
            self.reserve_action.setEnabled(True)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        add_icon = qta.icon("fa5s.book", color=LIGHT_GREEN_COLOR)
        modify_icon = qta.icon("fa5s.edit", color=LIGHT_GREEN_COLOR)
        delete_icon = qta.icon("fa5s.trash", color=LIGHT_GREEN_COLOR)
        borrow_icon = qta.icon("fa5s.hand-point-right", color=LIGHT_GREEN_COLOR)
        restore_books_icon = qta.icon("fa5s.undo", color=LIGHT_GREEN_COLOR)
        reserve_icon = qta.icon("fa5s.bookmark", color=LIGHT_GREEN_COLOR)

        self.add_action = QAction(add_icon, "Ajouter livre", self)
        self.add_action.setEnabled(False)
        toolbar.addAction(self.add_action)
        self.modify_action = QAction(modify_icon, "Modifier livre", self)
        self.modify_action.setEnabled(False)
        toolbar.addAction(self.modify_action)
        self.delete_action = QAction(delete_icon, "Supprimer livre", self)
        self.delete_action.setEnabled(False)
        self.delete_action.setShortcut("Ctrl+D")
        toolbar.addAction(self.delete_action)
        self.borrow_action = QAction(borrow_icon, "Emprunter livre", self)
        toolbar.addAction(self.borrow_action)
        self.restore_action = QAction(restore_books_icon, "Rendre livre", self)
        toolbar.addAction(self.restore_action)
        self.reserve_action = QAction(reserve_icon, "Réserver livre", self)
        toolbar.addAction(self.reserve_action)

        self.add_action.triggered.connect(self.controller.add_book)
        self.modify_action.triggered.connect(self.controller.modify_book)
        self.delete_action.triggered.connect(self.controller.delete_book)
        self.borrow_action.triggered.connect(self.controller.borrow_book)
        self.restore_action.triggered.connect(self.controller.restore_book)
        self.reserve_action.triggered.connect(self.controller.reserve_book)

        self.setStatusBar(QStatusBar(self))

    #############################
    # Debounce search functions #
    #############################
    def restart_search_timer(self):
        """Restart the search timer"""
        self.search_timer.start(500)

    def perform_search(self):
        """Perform a search when the timer times out"""
        search_text = self.search_input.text().strip()
        print(f"Searching for: {search_text}")
        self.controller.perform_search(search_text)
        self.controller.perform_search(search_text)
