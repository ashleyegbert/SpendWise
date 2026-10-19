import json
from pathlib import Path
from transaction import Transaction

DATA_FILE=Path(__file__).parent / "transactions.json"

def save_transaction(transactions):
    data=[]

    for transaction in transactions:
        data.append ({
            "title":transaction.title,
            "amount":transaction.amount,
            "category":transaction.category,
            "transaction_type":transaction.transaction_type,
            "transaction_date":transaction.transaction_date
        })

    with open(DATA_FILE,"w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def load_transactions():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    transactions = []

    for item in data:
        transaction = Transaction(
            title=item["title"],
            amount=item["amount"],
            category=item["category"],
            transaction_type=item["transaction_type"],
            transaction_date=item.get("transaction_date")
        )
        transactions.append(transaction)

    return transactions
