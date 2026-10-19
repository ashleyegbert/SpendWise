class Finance:
    def __init__(self):
        self.transactions=[]

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def calculate_total_income(self):
        total=0

        for transaction in self.transactions:
            if transaction.transaction_type=="income":
                total+=transaction.amount
        return total

    def calculate_total_expense(self):
        total=0

        for transaction in self.transactions:
            if transaction.transaction_type=="expense":
                total+=transaction.amount

        return total

    def calculate_balance(self):
        total_income=self.calculate_total_income()
        total_expense=self.calculate_total_expense()

        return total_income-total_expense

    def display_summary(self):
        total_income=self.calculate_total_income()
        total_expense=self.calculate_total_expense()
        balance=self.calculate_balance()

        print("\n===== SpendWise Financial Summary =====")
        print(f"Total Income:    €{total_income:.2f}")
        print(f"Total Expenses: €{total_expense:.2f}")
        print(f"Remaining Balance: €{balance:.2f}")
        print("=======================================")