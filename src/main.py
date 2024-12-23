import argparse
import sys

# from qt_material import apply_stylesheet
from PyQt6.QtWidgets import QApplication

from librarymanagementsystem.library_app import LibraryApp


def main():
    parser = argparse.ArgumentParser(
        description="Run LibraryApp with a specified role."
    )
    parser.add_argument(
        "--role",
        choices=["none", "user", "admin"],
        default="none",
        help="Specify the role to log in as (user or admin).",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme="dark_teal.xml")

    library_app = LibraryApp(role=args.role)
    library_app.run()

    app.exec()


if __name__ == "__main__":
    main()
    main()
