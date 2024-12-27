from librarymanagementsystem.entities.borrow_rules import BorrowRules
from librarymanagementsystem.repositories.borrow_rules_repository import (
    BorrowRulesRepository,
)
from librarymanagementsystem.repositories.database import Database


class BorrowRulesManager:
    def __init__(self, database: Database):
        self.borrow_rules_repository = BorrowRulesRepository(database)

    def read_all(self):
        return self.borrow_rules_repository.read_all()

    def modify(self, entity: BorrowRules):
        self.borrow_rules_repository.modify(entity)
