from librarymanagementsystem.entities.borrow_rules import BorrowRules
from librarymanagementsystem.repositories.abstract_repository import AbstractRepository
from librarymanagementsystem.repositories.database import Database


class BorrowRulesRepository(AbstractRepository):
    def __init__(self, database: Database):
        self.database = database

    def read_all(self):
        query = "SELECT * FROM regles_prets;"
        return self.database.exec_query(query)

    def modify(self, entity: BorrowRules):
        query = f"""
          UPDATE regles_prets
          SET duree_maximale = {entity.max_borrow_days},
            penalite_retard = {entity.late_penalty}
          WHERE id_regles_prets = {entity.id}
        """
        self.database.exec_query_with_commit(query)

    def insert(self, entity):
        return super().insert(entity)

    def delete(self, entity):
        return super().delete(entity)
