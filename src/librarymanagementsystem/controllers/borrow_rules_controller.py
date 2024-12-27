from librarymanagementsystem.entities.borrow_rules import BorrowRules
from librarymanagementsystem.managers.borrow_rules_manager import BorrowRulesManager
from librarymanagementsystem.repositories.database import Database


class BorrowRulesController:
    def __init__(self, database: Database, view):
        self.borrow_rules_model = None
        self.borrow_rules_manager = BorrowRulesManager(database)
        self.view = view
        self.borrow_rules_id = None
        self.max_borrow_days = None
        self.late_penalty = None

    def read_borrow_rules(self):
        df = self.borrow_rules_manager.read_all()
        if df.empty:
            return

        self.borrow_rules_id = df.loc[0, "id_regles_prets"]
        self.max_borrow_days = df.loc[0, "duree_maximale"]
        self.late_penalty = df.loc[0, "penalite_retard"]

    def modify_borrow_rules(self, max_borrow_days: int, late_penalty: int):
        entity = BorrowRules(max_borrow_days, late_penalty, self.borrow_rules_id)
        self.borrow_rules_manager.modify(entity)

    def borrow_rules_clicked(self):
        duree = self.view.max_borrow_days_input.text().strip()
        penalite = self.view.penalite_retard_input.text().strip()
        self.modify_borrow_rules(int(duree), int(penalite))
