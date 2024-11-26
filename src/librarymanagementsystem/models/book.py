import datetime
import uuid

from librarymanagementsystem.models.author import Author
from librarymanagementsystem.models.genre import Genre


class Book:
    def __init__(
        self,
        titre: str,
        auteurs: list[Author],
        genre: Genre,
        date_publication: datetime,
        date_emprunt: datetime = None,
        date_retour: datetime = None,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.titre = titre
        self.auteurs = auteurs
        self.genre = genre
        self.date_publication = date_publication
        self.date_emprunt = date_emprunt
        self.date_retour = date_retour

    def __str__(self):
        auteur_ids = [str(a.id) for a in self.auteurs]
        return f"{self.titre} by {auteur_ids} ({self.date_publication}) [{self.genre.name}] ; Date emprunt: {self.date_emprunt} ; Date retour: {self.date_retour}"

    @staticmethod
    def headers() -> list[str]:
        return [" Id ", " Titre ", " Auteurs ", " Genre ", " Date publication "]

    def to_list(self) -> list:
        # Returns a list of the book's attributes
        return [
            self.id,
            self.titre,
            self.auteurs[0].fullname,
            self.genre.name,
            self.date_publication,
        ]
