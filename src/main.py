import sys

# from qt_material import apply_stylesheet
from PyQt6.QtWidgets import QApplication

from librarymanagementsystem.controllers.library_controller import LibraryController


def main():
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme="dark_teal.xml")

    controller = LibraryController()
    controller.run()

    app.exec()


if __name__ == "__main__":
    main()
