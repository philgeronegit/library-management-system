from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.managers.book_manager import BookManager
from librarymanagementsystem.repositories.book_repository import BookRepository
from librarymanagementsystem.repositories.database import Database


@pytest.fixture
def mock_database():
    return MagicMock(spec=Database)


@pytest.fixture
def mock_book_repository(mock_database):
    repo = MagicMock(spec=BookRepository)
    return repo


@pytest.fixture
def book_manager(mock_book_repository, mock_database):
    # Mock the BookRepository creation
    with patch(
        "librarymanagementsystem.managers.book_manager.BookRepository",
        return_value=mock_book_repository,
    ):
        return BookManager(mock_database)


def test_read_all(book_manager, mock_book_repository):
    mock_df = pd.DataFrame({"ID": [1], "Titre": ["Book1"]})
    mock_book_repository.read_all.return_value = mock_df

    result = book_manager.read_all("all", "")

    assert result.equals(mock_df)
    mock_book_repository.read_all.assert_called_once_with("all", "")


def test_modify(book_manager, mock_book_repository):
    book = Book(id=1, title="Test", authors=[], genre=None, publication_date=None)
    user_id = 1

    book_manager.modify(book, user_id)

    mock_book_repository.modify.assert_called_once_with(book, user_id)


def test_delete(book_manager, mock_book_repository):
    book_id = 1
    user_id = 1

    book_manager.delete(book_id, user_id)

    mock_book_repository.delete.assert_called_once_with(book_id, user_id)


def test_insert(book_manager, mock_book_repository):
    book = Book(id=1, title="Test", authors=[], genre=None, publication_date=None)
    user_id = 1

    book_manager.insert(book, user_id)

    mock_book_repository.insert.assert_called_once_with(book, user_id)
