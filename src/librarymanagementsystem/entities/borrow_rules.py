class BorrowRules:
    def __init__(self, max_borrow_days: int, late_penalty: int, id: int):
        self.max_borrow_days = max_borrow_days
        self.late_penalty = late_penalty
        self.id = id
