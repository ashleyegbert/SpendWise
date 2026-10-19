from datetime import date

class Transaction:
    def __init__(self, title, amount,category,transaction_type, transaction_date=None):
        if not title.strip():
            raise ValueError("Title cannot be empty")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        if transaction_type not in ["expense", "income"]:
            raise ValueError("Transaction type must be either expense or income")

        self.title = title
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type

        self.transaction_date = (
            transaction_date or date.today().isoformat()
        )