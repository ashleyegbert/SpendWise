from transaction import Transaction
import pytest

def test_transaction_rejects_zero_amount():
    with pytest.raises(ValueError):
        Transaction(
            title="Groceries",
            amount=0,
            category="Food",
            transaction_type="expense"
        )

def test_transaction_rejects_invalid_type():
    with pytest.raises(ValueError):
        Transaction(
            title="Groceries",
            amount=25.0,
            category="Food",
            transaction_type="shopping"
        )
