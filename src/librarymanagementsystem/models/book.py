import datetime
import uuid


class Book:
    def __init__(
        self,
        titre: str,
        auteur: str,
        genre: str,
        date_publication: datetime,
        disponibilite: bool = True,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.date_publication = date_publication
        self.disponibilite = disponibilite

    def __str__(self):
        return f"{self.titre} - {self.auteur}"

    @staticmethod
    def headers() -> list[str]:
        return [
            " Id ",
            " Titre ",
            " Auteur ",
            " Genre ",
            " Date publication ",
            " Disponibilité ",
        ]

    def to_list(self) -> list:
        # Returns a list of the book's attributes
        return [
            self.id,
            self.titre,
            self.auteur,
            self.genre,
            self.date_publication,
            self.disponibilite,
        ]

    @staticmethod
    def from_list(data):
        # Returns a new Book object from a list
        # of data where the first element is the id
        # and the rest are the attributes of the book
        if len(data) != 6:
            raise ValueError("Invalid data")

        return Book(data[1], data[2], data[3], data[4], data[5])
