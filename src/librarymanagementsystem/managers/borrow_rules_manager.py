from librarymanagementsystem.repositories.borrow_rules_repository import (
    BorrowRulesRepository,
)
from librarymanagementsystem.repositories.database import Database


class BorrowRulesManager:
    def __init__(self, database: Database):
        self.borrow_rules_repository = BorrowRulesRepository(database)

    def read_borrow_rules(self):
        return self.borrow_rules_repository.read_borrow_rules()

    def modify_borrow_rules(self, duree_maximale_emprunt: int, penalite_par_jour: int):
        self.borrow_rules_repository.modify_borrow_rules(
            duree_maximale_emprunt, penalite_par_jour
        )
