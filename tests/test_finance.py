import finance
from finance import Finance
from transaction import Transaction

def test_add_transaction():
    finance = Finance()

    transaction = Transaction(
            title="Groceries",
            amount=34,
            category="Food",
            transaction_type="expense"
    )
    finance.add_transaction(transaction)

    assert len(finance.transactions) == 1
    assert finance.transactions[0].title=="Groceries"


def test_calculate_total_income():
    finance = Finance()

    salary = Transaction(
        title="Salary",
        amount=1000,
        category="Work",
        transaction_type="income"
    )

    groceries = Transaction(
        title="Groceries",
        amount=100,
        category="Food",
        transaction_type="expense"
    )

    finance.add_transaction(salary)
    finance.add_transaction(groceries)

    assert finance.calculate_total_income() == 1000

def test_calculate_total_expense():
    finance = Finance()

    salary = Transaction(
        title="Salary",
        amount=1000,
        category="Work",
        transaction_type="income"
    )

    groceries = Transaction(
        title="Groceries",
        amount=100,
        category="Food",
        transaction_type="expense"
    )

    transport = Transaction(
        title="Transport",
        amount=50,
        category="Travel",
        transaction_type="expense"
    )

    finance.add_transaction(groceries)
    finance.add_transaction(transport)
    finance.add_transaction(salary)

    assert finance.calculate_total_expense() == 150

def test_balance():
    finance = Finance()

    salary = Transaction(
        title="Salary",
        amount=1000,
        category="Work",
        transaction_type="income"
    )
    groceries = Transaction(
        title="Groceries",
        amount=100,
        category="Food",
        transaction_type="expense"
    )
    transport = Transaction(
        title="Transport",
        amount=50,
        category="Travel",
        transaction_type="expense"
    )

    finance.add_transaction(groceries)
    finance.add_transaction(transport)
    finance.add_transaction(salary)

    assert finance.calculate_balance() == 850