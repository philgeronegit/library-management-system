import datetime
import uuid

from librarymanagementsystem.models.author import Author
from librarymanagementsystem.models.genre import Genre


class Book:
    def __init__(
        self,
        titre: str,
        auteur: Author,
        genre: Genre,
        date_publication: datetime,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.date_publication = date_publication

    def __str__(self):
        return f"{self.titre} by {self.auteur.fullname} ({self.date_publication}) [{self.genre.name}]"

    @staticmethod
    def headers() -> list[str]:
        return [" Id ", " Titre ", " Auteur ", " Genre ", " Date publication "]

    def to_list(self) -> list:
        # Returns a list of the book's attributes
        return [
            self.id,
            self.titre,
            self.auteur.fullname,
            self.genre.name,
            self.date_publication,
        ]
