import datetime
import uuid

from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.entities.genre import Genre
from librarymanagementsystem.entities.user import User


class Book:
    def __init__(
        self,
        title: str,
        authors: list[Author],
        genre: Genre,
        publication_date: datetime,
        borrowing_date: datetime = None,
        borrowing_user: User = None,
        return_date: datetime = None,
        creation_date: datetime = None,
        added_by: User = None,
        modification_date: datetime = None,
        modified_by: User = None,
        deletion_date: datetime = None,
        deleted_by: User = None,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.title = title
        self.authors = authors
        self.genre = genre
        self.publication_date = publication_date
        self.borrowing_date = borrowing_date
        self.borrowing_user = borrowing_user
        self.return_date = return_date
        self.creation_date = creation_date
        self.added_by = added_by
        self.modification_date = modification_date
        self.modified_by = modified_by
        self.deletion_date = deletion_date
        self.deleted_by = deleted_by

    def __str__(self):
        author_ids = [str(a.id) for a in self.authors]
        return f"{self.title} by {author_ids} ({self.publication_date}) [{self.genre.name}] ; Date emprunt: {self.borrowing_date} ; Date retour: {self.return_date}"

    @staticmethod
    def headers() -> list[str]:
        return [" Id ", " Titre ", " Auteurs ", " Genre ", " Date publication "]

    def to_list(self) -> list:
        # Returns a list of the book's attributes
        authors = ", ".join([a.fullname for a in self.authors])
        return [
            self.id,
            self.title,
            authors,
            self.genre.name,
            self.publication_date,
        ]
