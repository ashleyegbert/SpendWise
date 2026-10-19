from finance import Finance
from transaction import Transaction
from storage import save_transaction, load_transactions

finance = Finance()
finance.transactions=load_transactions()

while True:
    print("\n===== SpendWise =====")
    print("1. Add transaction")
    print("2. View financial summary")
    print("3. Exit")

    choice =input("Enter your choice: ")

    if choice == "1":
        title=input("Enter your transaction title: ")
        amount=float(input("Enter your transaction amount: "))
        category=input("Enter your transaction category: ")
        transaction_type=input("Enter your transaction type(income/expense): ").lower()

        transaction=Transaction(
            title,
            amount,
            category,
            transaction_type
        )

        finance.add_transaction(transaction)
        save_transaction(finance.transactions)
        print("Transaction added")

    elif choice == "2":
        finance.display_summary()
    elif choice == "3":
        print("Thank you for using this program")
        break
    else:
        print("Please enter a valid choice")
