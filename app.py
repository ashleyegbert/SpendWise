import tkinter as tk
from tkinter import ttk,messagebox
from collections import defaultdict, Counter
from datetime import date, datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from transaction import Transaction
from finance import Finance
from storage import load_transactions, save_transaction

NAVY = "#142D4E"
BLUE = "#285CA8"
LIGHT_BLUE = "#EAF1FB"
WHITE = "#FFFFFF"
BACKGROUND = "#F4F7FC"
TEXT = "#243247"
MUTED = "#718096"
GREEN = "#16845B"
RED = "#C74747"

root=tk.Tk()
root.title("SpendWise")
root.geometry("1200x850")
root.minsize(950, 700)
root.configure(background=BACKGROUND)

style=ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    fieldbackground=WHITE,
    rowheight=30,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=LIGHT_BLUE,
    foreground=NAVY,
    font=("Segoe UI", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[("selected", BLUE)],
    foreground=[("selected", WHITE)]
)

finance = Finance()

try:
    finance.transactions = load_transactions()
except (OSError, ValueError, KeyError, TypeError) as error:
    messagebox.showerror(
        "Could not load transactions",
        f"SpendWise could not load your saved transactions.\n\n{error}"
    )
    finance.transactions = []

def format_money(amount):
    return f"€{amount:,.2f}"


def get_transaction_date(transaction):
    """Return a usable date for sorting and charting."""
    try:
        return date.fromisoformat(transaction.transaction_date)
    except (ValueError, TypeError, AttributeError):
        return date.today()

def make_button(parent, text, command, primary=True):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=BLUE if primary else WHITE,
        fg=WHITE if primary else NAVY,
        activebackground=NAVY if primary else LIGHT_BLUE,
        activeforeground=WHITE if primary else NAVY,
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=16,
        pady=10
    )

sidebar = tk.Frame(root, bg=NAVY, width=205)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="SpendWise",
    bg=NAVY,
    fg=WHITE,
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=22, pady=(30, 5))

tk.Label(
    sidebar,
    text="PERSONAL FINANCE",
    bg=NAVY,
    fg="#B8C9E2",
    font=("Segoe UI", 9, "bold")
).pack(anchor="w", padx=23, pady=(0, 35))


tk.Label(
    sidebar,
    text="▦  Dashboard",
    bg="#25456F",
    fg=WHITE,
    font=("Segoe UI", 11, "bold"),
    anchor="w",
    padx=18,
    pady=13
).pack(fill="x", padx=10)

tk.Label(
    sidebar,
    text="Track your money\nwith clarity.",
    bg=NAVY,
    fg="#C6D4E7",
    justify="left",
    font=("Segoe UI", 10),
    wraplength=160
).pack(side="bottom", anchor="w", padx=22, pady=25)


main = tk.Frame(root, bg=BACKGROUND)
main.pack(side="left", fill="both", expand=True)

header = tk.Frame(main, bg=BACKGROUND)
header.pack(fill="x", padx=25, pady=(22, 12))

header_text = tk.Frame(header, bg=BACKGROUND)
header_text.pack(side="left", fill="x", expand=True)

tk.Label(
    header_text,
    text="Financial Overview",
    bg=BACKGROUND,
    fg=NAVY,
    font=("Segoe UI", 23, "bold")
).pack(anchor="w")

tk.Label(
    header_text,
    text="Understand your income, spending and balance.",
    bg=BACKGROUND,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", pady=(4, 0))

summary_frame = tk.Frame(main, bg=BACKGROUND)
summary_frame.pack(fill="x", padx=20, pady=5)

summary_values = {}

card_details = [
    ("Total Income", GREEN, "income"),
    ("Total Expenses", RED, "expenses"),
    ("Remaining Balance", BLUE, "balance")
]

for index, (title, accent, key) in enumerate(card_details):
    card = tk.Frame(
        summary_frame,
        bg=WHITE,
        highlightbackground="#E1E8F2",
        highlightthickness=1
    )
    card.grid(
        row=0,
        column=index,
        sticky="nsew",
        padx=5,
        pady=5
    )

    tk.Label(
        card,
        text=title,
        bg=WHITE,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=15, pady=(14, 4))

    value_label = tk.Label(
        card,
        text="€0.00",
        bg=WHITE,
        fg=accent,
        font=("Segoe UI", 19, "bold")
    )
    value_label.pack(anchor="w", padx=15, pady=(0, 14))

    summary_values[key] = value_label

    summary_frame.grid_columnconfigure(index, weight=1)

charts_panel = tk.Frame(
    main,
    bg=WHITE,
    highlightbackground="#E1E8F2",
    highlightthickness=1
)
charts_panel.pack(fill="both", expand=True, padx=25, pady=12)

figure = Figure(figsize=(10, 5.8), dpi=100)
figure.patch.set_facecolor(WHITE)

ax_trend = figure.add_subplot(221)
ax_category = figure.add_subplot(222)
ax_comparison = figure.add_subplot(223)
ax_top = figure.add_subplot(224)

figure_canvas = FigureCanvasTkAgg(figure, master=charts_panel)
figure_canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=8,
    pady=8
)


recent_frame = tk.Frame(main, bg=BACKGROUND)
recent_frame.pack(fill="x", padx=25, pady=(0, 20))

recent_heading = tk.Frame(recent_frame, bg=BACKGROUND)
recent_heading.pack(fill="x", pady=(0, 8))

tk.Label(
    recent_heading,
    text="Recent Transactions",
    bg=BACKGROUND,
    fg=NAVY,
    font=("Segoe UI", 14, "bold")
).pack(side="left")

columns = ("date", "title", "category", "type", "amount")

transaction_table = ttk.Treeview(
    recent_frame,
    columns=columns,
    show="headings",
    height=5
)

transaction_table.tag_configure(
    "income",
    foreground="#16A34A"
)

transaction_table.tag_configure(
    "expense",
    foreground="#DC2626"
)

transaction_table.heading("date", text="Date")
transaction_table.heading("title", text="Description")
transaction_table.heading("category", text="Category")
transaction_table.heading("type", text="Type")
transaction_table.heading("amount", text="Amount")

transaction_table.column("date", width=105, anchor="center")
transaction_table.column("title", width=230)
transaction_table.column("category", width=140)
transaction_table.column("type", width=100, anchor="center")
transaction_table.column("amount", width=125, anchor="e")


def on_transaction_select(event):
    selected=transaction_table.selection()

    if selected:
        print("selected transaction:", selected[0])

transaction_table.pack(fill="x")

transaction_table.bind(
    "<<TreeviewSelect>>",
     on_transaction_select
)

def style_axis(axis,title):
    axis.set_title(title, loc="left", fontsize=10, fontweight="bold",
                   color=NAVY, pad=10)
    axis.set_facecolor(WHITE)
    axis.tick_params(axis="both", labelsize=8, colors=MUTED)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color("#DCE4EF")
    axis.spines["bottom"].set_color("#DCE4EF")
    axis.grid(axis="y", linestyle="--", alpha=0.25)
    axis.set_axisbelow(True)


def show_empty(axis, title):
    axis.clear()
    axis.set_title(title, loc="left", fontsize=10,
                   fontweight="bold", color=NAVY)
    axis.text(
        0.5,
        0.5,
        "Add transactions to see your data",
        ha="center",
        va="center",
        transform=axis.transAxes,
        fontsize=9,
        color=MUTED
    )
    axis.set_xticks([])
    axis.set_yticks([])
    for spine in axis.spines.values():
        spine.set_visible(False)

def refresh_dashboard():
    income = finance.calculate_total_income()
    expenses = finance.calculate_total_expense()
    balance = finance.calculate_balance()

    summary_values["income"].config(text=format_money(income))
    summary_values["expenses"].config(text=format_money(expenses))
    summary_values["balance"].config(
        text=format_money(balance),
        fg=GREEN if balance >= 0 else RED
    )

    for row in transaction_table.get_children():
        transaction_table.delete(row)

    sorted_transactions = sorted(
        finance.transactions,
        key=get_transaction_date,
        reverse=True
    )

    for transaction in sorted_transactions[:8]:
        amount_text = format_money(transaction.amount)

        if transaction.transaction_type == "expense":
            amount_text = "-" + amount_text
        else:
            amount_text = "+" + amount_text

        transaction_table.insert(
            "",
            "end",
            values=(
                get_transaction_date(transaction).isoformat(),
                transaction.title,
                transaction.category,
                transaction.transaction_type.title(),
                amount_text
            ),
            tags=(transaction.transaction_type.lower(),
                  )
        )

    expenses_by_date = defaultdict(float)
    expenses_by_category = defaultdict(float)
    income_by_category = defaultdict(float)
    expense_transactions = []

    for transaction in finance.transactions:
        transaction_date = get_transaction_date(transaction)

        if transaction.transaction_type == "expense":
            expenses_by_date[transaction_date] += transaction.amount
            expenses_by_category[transaction.category] += transaction.amount
            expense_transactions.append(transaction)

        elif transaction.transaction_type == "income":
            income_by_category[transaction.category] += transaction.amount

    ax_trend.clear()

    if expenses_by_date:
        dates = sorted(expenses_by_date)
        values = [expenses_by_date[d] for d in dates]

        ax_trend.plot(
            dates,
            values,
            marker="o",
            linewidth=2,
            markersize=4,
            color=BLUE
        )
        ax_trend.fill_between(dates, values, alpha=0.10, color=BLUE)
        style_axis(ax_trend, "Expenses over time")
        ax_trend.tick_params(axis="x", rotation=25)
        figure.autofmt_xdate(rotation=25)
    else:
        show_empty(ax_trend, "Expenses over time")

    # Chart 2: Expenses by category.
    ax_category.clear()

    if expenses_by_category:
        categories = sorted(
          expenses_by_category,
          key=expenses_by_category.get,
          reverse=True
        )
        values = [expenses_by_category[c] for c in categories]

        ax_category.barh(
            categories[::-1],
            values[::-1],
            color=BLUE
        )
        style_axis(ax_category, "Expenses by category")
        ax_category.set_xlabel("Amount (€)", fontsize=8, color=MUTED)
    else:
        show_empty(ax_category, "Expenses by category")

    # Chart 3: Income versus expenses.
    ax_comparison.clear()

    if finance.transactions:
        ax_comparison.bar(
            ["Income", "Expenses"],
            [income, expenses],
            color=[GREEN, RED],
            width=0.55
        )
        style_axis(ax_comparison, "Income vs expenses")
        ax_comparison.set_ylabel("Amount (€)", fontsize=8, color=MUTED)
    else:
        show_empty(ax_comparison, "Income vs expenses")

    # Chart 4: Largest individual expenses.
    ax_top.clear()

    if expense_transactions:
        largest = sorted(
            expense_transactions,
            key=lambda transaction: transaction.amount,
            reverse=True
        )[:5]

        labels = [
            transaction.title[:20]
            for transaction in largest
        ]
        values = [transaction.amount for transaction in largest]

        ax_top.barh(
            labels[::-1],
            values[::-1],
            color="#6B8EC7"
        )
        style_axis(ax_top, "Largest individual expenses")
        ax_top.set_xlabel("Amount (€)", fontsize=8, color=MUTED)
    else:
        show_empty(ax_top, "Largest individual expenses")

    figure.tight_layout(pad=2.2)
    figure_canvas.draw_idle()


# -------------------- ADD TRANSACTION WINDOW --------------------

def open_transaction_form():
    form = tk.Toplevel(root)
    form.title("Add Transaction - SpendWise")
    form.geometry("440x540")
    form.resizable(False, False)
    form.configure(bg=BACKGROUND)
    form.transient(root)
    form.grab_set()


    tk.Label(
        form,
        text="Add a Transaction",
        bg=BACKGROUND,
        fg=NAVY,
        font=("Segoe UI", 19, "bold")
    ).pack(anchor="w", padx=28, pady=(24, 4))

    tk.Label(
        form,
        text="Enter the details below.",
        bg=BACKGROUND,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=28, pady=(0, 16))

    fields = tk.Frame(form, bg=BACKGROUND)
    fields.pack(fill="x", padx=28)

    def add_field(label_text, row):
        tk.Label(
            fields,
            text=label_text,
            bg=BACKGROUND,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(row=row, column=0, sticky="w", pady=7)

    def make_entry(row, initial=""):
        entry = tk.Entry(
            fields,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        entry.grid(row=row, column=1, sticky="ew", pady=7, ipady=5)
        if initial:
            entry.insert(0, initial)
        return entry

    fields.grid_columnconfigure(1, weight=1)

    add_field("Description", 0)
    title_entry = make_entry(0)

    add_field("Amount (€)", 1)
    amount_entry = make_entry(1)

    add_field("Category", 2)
    category_var= tk.StringVar(value="Food")
    category_dropdown = ttk.Combobox(
        fields,
        textvariable=category_var,
        values=(
            "Food",
            "Transport",
            "Rent",
            "Bills",
            "Shopping",
            "Entertainment",
            "Health",
            "Education",
            "Salary",
            "Freelance",
            "Other"
        ),
        state="readonly",
        font=("Segoe UI", 11)
    )

    category_dropdown.grid(
        row=2,
        column=1,
        sticky="ew",
        pady=7,
        ipady=3,
    )
    add_field("Type", 3)
    type_var = tk.StringVar(value="expense")

    type_dropdown = ttk.Combobox(
        fields,
        textvariable=type_var,
        values=("expense", "income"),
        state="readonly",
        font=("Segoe UI", 11)
    )
    type_dropdown.grid(row=3, column=1, sticky="ew", pady=7, ipady=3)

    add_field("Date (YYYY-MM-DD)", 4)
    date_entry = make_entry(4, date.today().isoformat())

    tk.Label(
        form,
        text="Use a category such as Food, Transport, Salary or Rent.",
        bg=BACKGROUND,
        fg=MUTED,
        wraplength=370,
        justify="left",
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=28, pady=(8, 0))

    def save_new_transaction():
        title = title_entry.get().strip()
        category = category_var.get().strip()
        transaction_type = type_var.get().strip().lower()
        date_text = date_entry.get().strip()

        try:
            amount = float(amount_entry.get().strip())

            # Confirm the date is valid and follows YYYY-MM-DD.
            datetime.strptime(date_text, "%Y-%m-%d")

            transaction = Transaction(
                title=title,
                amount=amount,
                category=category,
                transaction_type=transaction_type,
                transaction_date=date_text
            )

            # Add first, then save. Roll back if saving fails.
            finance.add_transaction(transaction)

            try:
                save_transaction(finance.transactions)
            except (OSError, TypeError, ValueError) as error:
                finance.transactions.pop()
                messagebox.showerror(
                    "Save failed",
                    f"The transaction could not be saved.\n\n{error}",
                    parent=form
                )
                return

            refresh_dashboard()
            form.destroy()

        except ValueError as error:
            messagebox.showerror(
                "Check your entries",
                f"Please check the amount, date and transaction details.\n\n{error}",
                parent=form
            )

    buttons = tk.Frame(form, bg=BACKGROUND)
    buttons.pack(fill="x", padx=28, pady=22)

    make_button(
        buttons,
        "Save Transaction",
        save_new_transaction
    ).pack(side="left")

    make_button(
        buttons,
        "Cancel",
        form.destroy,
        primary=False
    ).pack(side="right")

    title_entry.focus_set()


def open_form():
    print("opening form")

    try:
        open_transaction_form()
    except Exception as error:
        messagebox.showerror(
            "Form error",
            f"{type(error).__name__}:{error}",
            parent=root
        )
        raise
make_button(
    header,
    "+ Add Transaction",
    open_form
).pack(side="right", padx=(12, 0))

refresh_dashboard()
root.mainloop()
