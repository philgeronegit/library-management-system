import uuid


class Author:
    def __init__(
        self,
        firstname: str,
        lastname: str,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return f"Author(firstname={self.firstname}, lastname={self.lastname})"

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"

    @staticmethod
    def headers() -> list[str]:
        return [" Id ", " Prénom ", " Nom "]

    def to_list(self) -> list:
        # Returns a list of the author's attributes
        return [
            self.id,
            self.firstname,
            self.lastname,
        ]

    @staticmethod
    def from_list(data):
        # Returns a new author object from a list
        # of data where the first element is the id
        # and the rest are the attributes of the author
        if len(data) != 3:
            raise ValueError("Invalid data")

        return Author(data[1], data[2])
