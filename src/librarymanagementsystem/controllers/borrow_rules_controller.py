from librarymanagementsystem.managers.borrow_rules_manager import BorrowRulesManager
from librarymanagementsystem.repositories.database import Database


class BorrowRulesController:
    def __init__(self, database: Database, view):
        self.authors_model = None
        self.author_manager = BorrowRulesManager(database)
        self.view = view
        self.duree_maximale_emprunt = None
        self.penalite_retard = None

    def read_borrow_rules(self):
        df = self.author_manager.read_borrow_rules()
        if df.empty:
            return

        self.duree_maximale_emprunt = df.loc[0, "duree_maximale_emprunt"]
        self.penalite_retard = df.loc[0, "penalite_retard"]

    def modify_borrow_rules(self, duree_maximale_emprunt: int, penalite_par_jour: int):
        self.author_manager.modify_borrow_rules(
            duree_maximale_emprunt, penalite_par_jour
        )

    def save_regles_prets_clicked(self):
        duree = self.view.duree_maximale_emprunt_input.text().strip()
        penalite = self.view.penalite_retard_input.text().strip()
        self.modify_borrow_rules(int(duree), int(penalite))
        self.book_controller.read_books()
        self.update_viewport_books()
