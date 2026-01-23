from unittest.mock import MagicMock

import pandas as pd
import pytest

from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.repositories.author_repository import AuthorRepository
from librarymanagementsystem.repositories.database import Database


@pytest.fixture
def mock_database():
    db = MagicMock(spec=Database)
    return db


@pytest.fixture
def author_repository(mock_database):
    return AuthorRepository(mock_database)


def test_read_all(author_repository, mock_database):
    mock_df = pd.DataFrame(
        {"ID": [1, 2], "Prénom": ["John", "Jane"], "Nom": ["Doe", "Smith"]}
    )
    mock_database.exec_query.return_value = mock_df

    result = author_repository.read_all()

    assert isinstance(result, pd.DataFrame)
    mock_database.exec_query.assert_called_once()


def test_insert(author_repository, mock_database):
    author = Author(firstname="John", lastname="Doe")

    author_repository.insert(author)

    mock_database.exec_query_with_commit.assert_called_once()


def test_modify(author_repository, mock_database):
    author = Author(id=1, firstname="John", lastname="Doe")

    author_repository.modify(author)

    mock_database.exec_query_with_commit.assert_called_once()


def test_delete(author_repository, mock_database):
    author_id = 1

    author_repository.delete(author_id)

    mock_database.exec_query_with_commit.assert_called_once()
