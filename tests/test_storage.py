
import storage
from transaction import Transaction


def test_save_and_load_transactions(tmp_path, monkeypatch):
    test_file = tmp_path / "transactions.json"
    monkeypatch.setattr(storage, "DATA_FILE", test_file)

    original_transactions = [
        Transaction(
            title="Salary",
            amount=1000,
            category="Work",
            transaction_type="income"
        ),
        Transaction(
            title="Groceries",
            amount=100,
            category="Food",
            transaction_type="expense"
        )
    ]

    storage.save_transaction(original_transactions)
    loaded_transactions = storage.load_transactions()

    assert len(loaded_transactions) == 2
    assert loaded_transactions[0].title == "Salary"
    assert loaded_transactions[0].amount == 1000
    assert loaded_transactions[1].title == "Groceries"
    assert loaded_transactions[1].transaction_type == "expense"
