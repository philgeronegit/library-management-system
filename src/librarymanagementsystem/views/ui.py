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
    QMessageBox,
    QPushButton,
    QRadioButton,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from librarymanagementsystem.entities.user import User
from librarymanagementsystem.utils.constants import (
    ALL_BOOKS,
    AVAILABLE_BOOKS,
    BORROWED_BOOKS,
    DELETED_BOOKS,
    LATE_BOOKS,
)
from librarymanagementsystem.views.components.clearable_line_edit import (
    ClearableLineEdit,
)
from librarymanagementsystem.views.components.custom_table_view import (
    CustomTableView,
    CustomTableViewBook,
    CustomTableViewUser,
)
from librarymanagementsystem.views.constants import LIGHT_GREEN_COLOR
from librarymanagementsystem.views.utils import input_factory


class LibraryView(QMainWindow):
    def __init__(self, library_app=None):
        super().__init__()
        icon = qta.icon("fa5s.book")
        self.setWindowIcon(icon)
        self.setWindowTitle("Librairie")

        self.library_app = library_app
        self.create_ui()

        self.setMinimumWidth(1024)
        self.setMinimumHeight(768)
        self.resize(1200, 800)

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
        self.user_add_action = self.user_menu.addAction("Ajouter")
        self.user_add_action.triggered.connect(self.user_add)
        self.author_menu = self.menu.addMenu("Auteurs")
        self.author_add_action = self.author_menu.addAction("Ajouter")
        self.author_add_action.triggered.connect(self.author_add)
        self.genre_menu = self.menu.addMenu("Genres")
        self.genre_add_action = self.genre_menu.addAction("Ajouter")
        self.genre_add_action.triggered.connect(self.genre_add)

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

        self.users_tab = QWidget()
        self.users_tab_layout = QVBoxLayout()
        self.users_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.users_tab.setLayout(self.users_tab_layout)
        self.tab.addTab(self.users_tab, "Utilisateurs")

        self.authors_tab = QWidget()
        self.authors_tab_layout = QVBoxLayout()
        self.authors_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.authors_tab.setLayout(self.authors_tab_layout)
        self.tab.addTab(self.authors_tab, "Auteurs")

        self.genres_tab = QWidget()
        self.genres_tab_layout = QVBoxLayout()
        self.genres_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.genres_tab.setLayout(self.genres_tab_layout)
        self.tab.addTab(self.genres_tab, "Genres")

        self.borrow_rules_tab = QWidget()
        self.borrow_rules_tab_layout = QVBoxLayout()
        self.borrow_rules_tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout = QFormLayout()
        self.borrow_rules_tab_layout.addLayout(form_layout)
        users_filter_label, self.max_borrow_days_input = input_factory(
            "Durée maximale emprunt :"
        )
        form_layout.addRow(users_filter_label, self.max_borrow_days_input)
        users_filter_label, self.penalite_retard_input = input_factory(
            "Pénalité de retard :"
        )
        form_layout.addRow(users_filter_label, self.penalite_retard_input)
        self.save_regles_prets_button = QPushButton("Sauver")
        self.borrow_rules_tab_layout.addWidget(self.save_regles_prets_button)

        self.borrow_rules_tab.setLayout(self.borrow_rules_tab_layout)
        self.tab.addTab(self.borrow_rules_tab, "Règles de prêts")

        self.layout.addWidget(self.tab)

        self.search_input = ClearableLineEdit()
        self.search_input.setPlaceholderText("Recherche de livres, auteurs, genres.")
        self.livres_tab_layout.addWidget(self.search_input)

        self.filter_layout = QHBoxLayout()
        self.filter_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.all_books_radio = QRadioButton("Tous les livres")
        self.all_books_radio.setProperty("type", ALL_BOOKS)

        self.all_books_radio.setChecked(True)
        self.available_books_radio = QRadioButton("Livres disponibles")
        self.available_books_radio.setProperty("type", AVAILABLE_BOOKS)

        self.borrowed_books_radio = QRadioButton("Livres empruntés")
        self.borrowed_books_radio.setProperty("type", BORROWED_BOOKS)

        self.deleted_books_radio = QRadioButton("Livres supprimés")
        self.deleted_books_radio.setProperty("type", DELETED_BOOKS)

        self.late_books_radio = QRadioButton("Retours en retard")
        self.late_books_radio.setProperty("type", LATE_BOOKS)
        self.user_combo_box = QComboBox()

        self.filter_layout.addWidget(self.all_books_radio)
        self.filter_layout.addWidget(self.available_books_radio)
        self.filter_layout.addWidget(self.borrowed_books_radio)
        self.filter_layout.addWidget(self.deleted_books_radio)
        self.filter_layout.addWidget(self.late_books_radio)
        self.users_filter_label = QLabel("Utilisateurs")
        self.filter_layout.addWidget(self.users_filter_label)
        self.filter_layout.addWidget(self.user_combo_box)
        self.livres_tab_layout.addLayout(self.filter_layout)

        self.table_views = []
        self.books_table = CustomTableViewBook("books", self.library_app)
        self.table_views.append(self.books_table)
        self.livres_tab_layout.addWidget(self.books_table)

        self.users_table = CustomTableViewUser("users", self.library_app)
        self.table_views.append(self.users_table)
        self.users_tab_layout.addWidget(self.users_table)

        self.authors_table = CustomTableView("authors", self.library_app)
        self.table_views.append(self.authors_table)
        self.authors_tab_layout.addWidget(self.authors_table)

        self.genres_table = CustomTableView("genres", self.library_app)
        self.table_views.append(self.genres_table)
        self.genres_tab_layout.addWidget(self.genres_table)

        self.setCentralWidget(self.centralWidget)

        self.create_toolbar()

        # Create a QTimer for debouncing
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)

        # Connect the textChanged signal to restart the timer
        self.search_input.textChanged.connect(self.restart_search_timer)

    def handle_radio_button_toggled(self):
        rbtn = self.sender()
        self.library_app.book_controller.filter_change(rbtn.property("type"))

    def closeEvent(self, event):
        event.accept()
        sys.exit()

    def login(self):
        self.library_app.login_controller.login(
            self.library_app.user_controller.users_model
        )

    def logout(self):
        self.library_app.login_controller.logout()

    def user_add(self):
        self.tab.setCurrentIndex(1)
        self.library_app.user_controller.add()

    def author_add(self):
        self.tab.setCurrentIndex(2)
        self.library_app.author_controller.add()

    def genre_add(self):
        self.tab.setCurrentIndex(3)
        self.library_app.genre_controller.add()

    def set_tab_visibility(self, is_visible: bool):
        self.tab.setTabVisible(1, is_visible)
        self.tab.setTabVisible(2, is_visible)
        self.tab.setTabVisible(3, is_visible)
        self.tab.setTabVisible(4, is_visible)

    def update_user_actions(self, user: User = None):
        """Update the actions available to the user"""
        if user is None:
            self.author_menu.setEnabled(False)
            self.genre_menu.setEnabled(False)
            self.user_add_action.setVisible(False)
            self.users_filter_label.setVisible(False)
            self.user_combo_box.setVisible(False)
            self.deleted_books_radio.setVisible(False)
            self.late_books_radio.setVisible(False)
            self.login_action.setEnabled(True)
            self.logout_action.setEnabled(False)
            self.set_tab_visibility(False)
            self.add_action.setEnabled(False)
            self.modify_action.setEnabled(False)
            self.delete_action.setEnabled(False)
            self.borrow_action.setEnabled(False)
            self.restore_action.setEnabled(False)
            self.reserve_action.setEnabled(False)
            for table in self.table_views:
                table.add_action.setEnabled(False)
                table.modify_action.setEnabled(False)
                table.delete_action.setEnabled(False)
                if table.name == "books":
                    table.borrow_action.setEnabled(False)
                    table.restore_action.setEnabled(False)
            return

        self.login_action.setEnabled(False)
        self.logout_action.setEnabled(True)

        if user.is_admin:
            self.author_menu.setEnabled(True)
            self.genre_menu.setEnabled(True)
            self.user_add_action.setVisible(True)
            self.users_filter_label.setVisible(True)
            self.user_combo_box.setVisible(True)
            self.deleted_books_radio.setVisible(True)
            self.late_books_radio.setVisible(True)
            self.set_tab_visibility(True)
            self.add_action.setEnabled(True)
            self.modify_action.setEnabled(True)
            self.delete_action.setEnabled(True)
            self.borrow_action.setEnabled(True)
            self.restore_action.setEnabled(True)
            self.reserve_action.setEnabled(True)
            for table in self.table_views:
                table.add_action.setEnabled(True)
                table.modify_action.setEnabled(True)
                table.delete_action.setEnabled(True)
                if table.name == "books":
                    table.borrow_action.setEnabled(True)
                    table.restore_action.setEnabled(True)
        else:
            self.author_menu.setEnabled(False)
            self.genre_menu.setEnabled(False)
            self.user_add_action.setVisible(False)
            self.users_filter_label.setVisible(False)
            self.user_combo_box.setVisible(False)
            self.deleted_books_radio.setVisible(False)
            self.late_books_radio.setVisible(False)
            self.set_tab_visibility(False)
            self.add_action.setEnabled(False)
            self.modify_action.setEnabled(False)
            self.delete_action.setEnabled(False)
            self.borrow_action.setEnabled(True)
            self.restore_action.setEnabled(True)
            self.reserve_action.setEnabled(True)
            for table in self.table_views:
                table.add_action.setEnabled(False)
                table.modify_action.setEnabled(False)
                table.delete_action.setEnabled(False)
                if table.name == "books":
                    table.borrow_action.setEnabled(True)
                    table.restore_action.setEnabled(True)

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
        self.borrow_action.setEnabled(False)
        toolbar.addAction(self.borrow_action)
        self.restore_action = QAction(restore_books_icon, "Rendre livre", self)
        self.restore_action.setEnabled(False)
        toolbar.addAction(self.restore_action)
        self.reserve_action = QAction(reserve_icon, "Réserver livre", self)
        self.reserve_action.setEnabled(False)
        toolbar.addAction(self.reserve_action)

        self.setStatusBar(QStatusBar(self))

    def connect_signals(self):
        self.all_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.available_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.borrowed_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.deleted_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.late_books_radio.toggled.connect(self.handle_radio_button_toggled)
        self.add_action.triggered.connect(self.library_app.book_controller.add)
        self.modify_action.triggered.connect(self.library_app.book_controller.modify)
        self.delete_action.triggered.connect(self.library_app.book_controller.delete)
        self.borrow_action.triggered.connect(
            self.library_app.book_controller.borrow_book
        )
        self.restore_action.triggered.connect(
            self.library_app.book_controller.restore_book
        )
        self.reserve_action.triggered.connect(
            self.library_app.book_controller.reserve_book
        )
        self.save_regles_prets_button.clicked.connect(self.borrow_rules_clicked)
        self.user_combo_box.currentIndexChanged.connect(
            self.library_app.book_controller.user_combo_box_changed
        )
        for table in self.table_views:
            table.connect_signals()

    def borrow_rules_clicked(self):
        self.library_app.borrow_rules_controller.borrow_rules_clicked()
        self.library_app.book_controller.read_all()
        QMessageBox.information(self, "Succès", "Règles de prêts sauvegardées.")

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
        self.library_app.book_controller.perform_search(search_text)
