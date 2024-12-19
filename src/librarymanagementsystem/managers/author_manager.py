from librarymanagementsystem.entities.author import Author
from librarymanagementsystem.repositories.author_repository import AuthorRepository
from librarymanagementsystem.repositories.database import Database


class AuthorManager:
    def __init__(self, database: Database):
        self.author_repository = AuthorRepository(database)

    def read_all(self):
        return self.author_repository.read_all()

    def insert(self, author: Author):
        self.author_repository.insert(author)

    def modify(self, author: Author):
        self.author_repository.modify(author)

    def delete(self, author_id: int):
        self.author_repository.delete(author_id)
