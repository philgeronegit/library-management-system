from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from librarymanagementsystem.controllers.book_controller import BookController
from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.managers.book_manager import BookManager
from librarymanagementsystem.managers.loan_manager import LoanManager
from librarymanagementsystem.repositories.database import Database
from librarymanagementsystem.views.table_model import TableModel


@pytest.fixture
def mock_database():
    return MagicMock(spec=Database)


@pytest.fixture
def mock_view():
    view = MagicMock()
    view.books_table = MagicMock()
    view.statusBar = MagicMock()
    view.statusBar.return_value.showMessage = MagicMock()
    view.user_combo_box = MagicMock()
    return view


@pytest.fixture
def mock_controllers():
    return {
        "author_controller": MagicMock(),
        "genre_controller": MagicMock(),
        "user_controller": MagicMock(),
        "login_controller": MagicMock(),
        "borrow_rules_controller": MagicMock(),
        "dialog_manager": MagicMock(),
    }


@pytest.fixture
def book_controller(mock_database, mock_view, mock_controllers):
    with (
        patch(
            "librarymanagementsystem.controllers.book_controller.BookManager"
        ) as mock_bm,
        patch(
            "librarymanagementsystem.controllers.book_controller.LoanManager"
        ) as mock_lm,
        patch(
            "librarymanagementsystem.controllers.book_controller.TableModel"
        ) as mock_tm,
    ):
        controller = BookController(mock_database, mock_view, **mock_controllers)
        return controller


def test_filter_change(book_controller):
    book_controller.filter_change("all")
    assert book_controller.filter_type == "all"


def test_read_all(book_controller):
    mock_df = pd.DataFrame({"ID": [1], "Titre": ["Book1"]})
    book_controller.book_manager.read_all.return_value = mock_df

    book_controller.read_all()

    book_controller.book_manager.read_all.assert_called_once_with("all", "")
    # Check that TableModel was created with the df
    # Since we mocked TableModel, we can check if it was called


def test_delete(book_controller, mock_controllers):
    book = Book(id=1, title="Test", authors=[], genre=None, publication_date=None)
    book_controller.get_selected_book = MagicMock(return_value=book)
    mock_controllers["login_controller"].selected_user.id = 1
    mock_controllers["dialog_manager"].delete_book.return_value = True

    with patch.object(book_controller, "read_all") as mock_read_all:
        book_controller.delete()

        book_controller.book_manager.delete.assert_called_once_with(1, 1)
        mock_read_all.assert_called_once()


def test_get_selected_book_no_selection(book_controller, mock_view):
    from librarymanagementsystem.utils.selection import get_selected_indexes

    with patch(
        "librarymanagementsystem.controllers.book_controller.get_selected_indexes",
        return_value=[],
    ):
        result = book_controller.get_selected_book()

    assert result is None


# More tests can be added for other methods
