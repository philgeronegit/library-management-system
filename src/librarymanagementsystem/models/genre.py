import uuid


class Genre:
    def __init__(
        self,
        name: str,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.name = name

    def __str__(self):
        return f"Genre(name={self.name})"

    @staticmethod
    def headers() -> list[str]:
        return [" Id ", " Nom "]

    def to_list(self) -> list:
        # Returns a list of the genre's attributes
        return [self.id, self.name]

    @staticmethod
    def from_list(data):
        # Returns a new genre object from a list
        # of data where the first element is the id
        # and the rest are the attributes of the genre
        if len(data) != 2:
            raise ValueError("Invalid data")

        return Genre(data[1])
