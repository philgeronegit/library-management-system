import uuid


class User:
    def __init__(
        self,
        username: str,
        email: str,
        status: str,
        password: str,
        id: int = None,
        role: str = "user",
    ):
        self.id = id or int(uuid.uuid4())
        self.username = username
        self.email = email
        self.status = status
        self.password = password
        self.role = role

    def __str__(self):
        return f"User(username={self.username}, contact={self.email}, status={self.status}, password={self.password})"

    @staticmethod
    def headers() -> list[str]:
        return [" Id ", " Nom ", " Mot de passe ", " Email ", " Status "]

    def to_list(self) -> list:
        # Returns a list of the user's attributes
        return [
            self.id,
            self.username,
            self.email,
            self.status,
            self.password,
        ]

    @staticmethod
    def from_list(data):
        # Returns a new User object from a list
        # of data where the first element is the id
        # and the rest are the attributes of the user
        if len(data) != 5:
            raise ValueError("Invalid data")

        return User(data[1], data[2], data[3], data[4])
