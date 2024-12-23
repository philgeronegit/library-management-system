from librarymanagementsystem.repositories.database import Database


class BorrowRulesRepository:
    def __init__(self, database: Database):
        self.database = database

    def read_borrow_rules(self):
        query = "SELECT * FROM regles_prets;"
        return self.database.exec_query(query)

    def modify_borrow_rules(self, duree_maximale_emprunt: int, penalite_par_jour: int):
        query = f"""
          UPDATE regles_prets
          SET duree = {duree_maximale_emprunt}, penalite = {penalite_par_jour}
          WHERE id_regles_prets = 1
        """
        self.database.exec_query_with_commit(query)
