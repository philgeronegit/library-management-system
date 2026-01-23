from unittest.mock import MagicMock

import pandas as pd
import pytest

from librarymanagementsystem.entities.book import Book
from librarymanagementsystem.entities.genre import Genre
from librarymanagementsystem.repositories.book_repository import BookRepository
from librarymanagementsystem.repositories.database import Database


@pytest.fixture
def mock_database():
    db = MagicMock(spec=Database)
    return db


@pytest.fixture
def book_repository(mock_database):
    return BookRepository(mock_database)


def test_read_all(book_repository, mock_database):
    # Mock the exec_query to return a sample DataFrame
    mock_df = pd.DataFrame(
        {
            "ID": [1, 2],
            "Titre": ["Book1", "Book2"],
            "Auteurs": ["Author1", "Author2"],
            "Genre": ["Fiction", "Non-Fiction"],
        }
    )
    mock_database.exec_query.return_value = mock_df

    result = book_repository.read_all()

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    mock_database.exec_query.assert_called_once()


def test_insert(book_repository, mock_database):
    genre = Genre(id=1, name="Fiction")
    book = Book(title="Test Book", authors=[], genre=genre, publication_date=None)
    user_id = 1

    book_repository.insert(book, user_id)

    # Assert that getEngine was called
    mock_database.getEngine.assert_called_once()


def test_modify(book_repository, mock_database):
    genre = Genre(id=1, name="Fiction")
    book = Book(id=1, title="Test Book", authors=[], genre=genre, publication_date=None)
    user_id = 1

    book_repository.modify(book, user_id)

    mock_database.exec_queries_with_commit.assert_called_once()


def test_delete(book_repository, mock_database):
    book_id = 1
    user_id = 1

    book_repository.delete(book_id, user_id)

    mock_database.exec_queries_with_commit.assert_called_once()


def test_reserve_book(book_repository, mock_database):
    book_id = 1
    user_id = 1

    book_repository.reserve_book(book_id, user_id)

    mock_database.exec_query_with_commit.assert_called_once()


def test_borrow_book(book_repository, mock_database):
    book_id = 1
    user_id = 1
    borrow_rules_id = 1

    book_repository.borrow_book(book_id, user_id, borrow_rules_id)

    mock_database.exec_query_with_commit.assert_called_once()


def test_return_book(book_repository, mock_database):
    book_id = 1
    user_id = 1

    book_repository.return_book(book_id, user_id)

    mock_database.exec_query_with_commit.assert_called_once()
