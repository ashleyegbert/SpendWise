import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
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
NAV_ACTIVE = "#25456F"

CATEGORIES = (
    "Food", "Transport", "Rent", "Bills", "Shopping", "Entertainment",
    "Health", "Education", "Salary", "Freelance", "Other"
)

root = tk.Tk()
root.title("SpendWise")
root.geometry("1200x850")
root.minsize(950, 700)
root.configure(background=BACKGROUND)

style = ttk.Style()
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


# -------------------- HELPERS --------------------

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


def page_header(parent, title, subtitle):
    """Create a header row. Returns the header frame."""
    header = tk.Frame(parent, bg=BACKGROUND)
    header.pack(fill="x", padx=25, pady=(22, 12))

    text_frame = tk.Frame(header, bg=BACKGROUND)
    text_frame.pack(side="left", fill="x", expand=True)

    tk.Label(
        text_frame, text=title, bg=BACKGROUND, fg=NAVY,
        font=("Segoe UI", 23, "bold")
    ).pack(anchor="w")

    tk.Label(
        text_frame, text=subtitle, bg=BACKGROUND, fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(4, 0))

    return header


columns = ("date", "title", "category", "type", "amount")


def setup_table_columns(table):
    table.tag_configure("income", foreground="#16A34A")
    table.tag_configure("expense", foreground="#DC2626")

    table.heading("date", text="Date")
    table.heading("title", text="Description")
    table.heading("category", text="Category")
    table.heading("type", text="Type")
    table.heading("amount", text="Amount")

    table.column("date", width=105, anchor="center")
    table.column("title", width=260)
    table.column("category", width=140)
    table.column("type", width=100, anchor="center")
    table.column("amount", width=125, anchor="e")


def transaction_row_values(transaction):
    sign = "-" if transaction.transaction_type == "expense" else "+"
    return (
        get_transaction_date(transaction).isoformat(),
        transaction.title,
        transaction.category,
        transaction.transaction_type.title(),
        sign + format_money(transaction.amount)
    )


# -------------------- SIDEBAR / NAVIGATION --------------------

sidebar = tk.Frame(root, bg=NAVY, width=205)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar, text="SpendWise", bg=NAVY, fg=WHITE,
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=22, pady=(30, 5))

tk.Label(
    sidebar, text="PERSONAL FINANCE", bg=NAVY, fg="#B8C9E2",
    font=("Segoe UI", 9, "bold")
).pack(anchor="w", padx=23, pady=(0, 35))

nav_buttons = {}


def make_nav_button(key, text):
    button = tk.Button(
        sidebar,
        text=text,
        command=lambda: show_page(key),
        bg=NAVY,
        fg=WHITE,
        activebackground=NAV_ACTIVE,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 11, "bold"),
        anchor="w",
        padx=18,
        pady=13
    )
    button.pack(fill="x", padx=10, pady=2)
    nav_buttons[key] = button


make_nav_button("dashboard", "  Dashboard")
make_nav_button("transactions", "  Transactions")
make_nav_button("report","Report")

tk.Label(
    sidebar,
    text="Track your money\nwith clarity.",
    bg=NAVY,
    fg="#C6D4E7",
    justify="left",
    font=("Segoe UI", 10),
    wraplength=160
).pack(side="bottom", anchor="w", padx=22, pady=25)


# -------------------- PAGE CONTAINER --------------------

main = tk.Frame(root, bg=BACKGROUND)
main.pack(side="left", fill="both", expand=True)

dashboard_page = tk.Frame(main, bg=BACKGROUND)
transactions_page = tk.Frame(main, bg=BACKGROUND)
reports_page=tk.Frame(main, bg=BACKGROUND)

pages = {
    "dashboard": dashboard_page,
    "transactions": transactions_page,
    "report":reports_page,
}


def show_page(name):
    for page in pages.values():
        page.pack_forget()
    pages[name].pack(fill="both", expand=True)

    for key, button in nav_buttons.items():
        button.config(bg=NAV_ACTIVE if key == name else NAVY)

    if name == "dashboard":
        # Redraw once the page is visible so the charts fit properly.
        root.after_idle(refresh_dashboard)
    elif name=="transactions":
        refresh_transactions()


# ======================================================================
#                           DASHBOARD PAGE
# ======================================================================

dashboard_header = page_header(
    dashboard_page,
    "Financial Overview",
    "Understand your income, spending and balance."
)

summary_frame = tk.Frame(dashboard_page, bg=BACKGROUND)
summary_frame.pack(fill="x", padx=20, pady=5)

summary_values = {}

card_details = [
    ("Total Income", GREEN, "income"),
    ("Total Expenses", RED, "expenses"),
    ("Remaining Balance", BLUE, "balance")
]

for index, (title, accent, key) in enumerate(card_details):
    card = tk.Frame(
        summary_frame, bg=WHITE,
        highlightbackground="#E1E8F2", highlightthickness=1
    )
    card.grid(row=0, column=index, sticky="nsew", padx=5, pady=5)

    tk.Label(
        card, text=title, bg=WHITE, fg=MUTED, font=("Segoe UI", 10)
    ).pack(anchor="w", padx=15, pady=(14, 4))

    value_label = tk.Label(
        card, text="€0.00", bg=WHITE, fg=accent,
        font=("Segoe UI", 19, "bold")
    )
    value_label.pack(anchor="w", padx=15, pady=(0, 14))

    summary_values[key] = value_label
    summary_frame.grid_columnconfigure(index, weight=1)


charts_panel = tk.Frame(
    dashboard_page, bg=WHITE,
    highlightbackground="#E1E8F2", highlightthickness=1
)
charts_panel.pack(fill="both", expand=True, padx=25, pady=8)

figure = Figure(figsize=(10, 3.5), dpi=100)
figure.patch.set_facecolor(WHITE)

ax_trend = figure.add_subplot(221)
ax_category = figure.add_subplot(222)
ax_comparison = figure.add_subplot(223)
ax_top = figure.add_subplot(224)

figure_canvas = FigureCanvasTkAgg(figure, master=charts_panel)
figure_canvas.get_tk_widget().configure(width=800, height=300)
figure_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)


def style_axis(axis, title):
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
        0.5, 0.5, "Add transactions to see your data",
        ha="center", va="center", transform=axis.transAxes,
        fontsize=9, color=MUTED
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


    expenses_by_date = defaultdict(float)
    expenses_by_category = defaultdict(float)
    expense_transactions = []

    for transaction in finance.transactions:
        if transaction.transaction_type == "expense":
            expenses_by_date[get_transaction_date(transaction)] += transaction.amount
            expenses_by_category[transaction.category] += transaction.amount
            expense_transactions.append(transaction)


    ax_trend.clear()
    if expenses_by_date:
        dates = sorted(expenses_by_date)
        values = [expenses_by_date[d] for d in dates]
        ax_trend.plot(dates, values, marker="o", linewidth=2,
                      markersize=4, color=BLUE)
        ax_trend.fill_between(dates, values, alpha=0.10, color=BLUE)
        style_axis(ax_trend, "Expenses over time")
        ax_trend.tick_params(axis="x", rotation=25)
    else:
        show_empty(ax_trend, "Expenses over time")

    # Chart 2: expenses by category.
    ax_category.clear()
    if expenses_by_category:
        categories = sorted(
            expenses_by_category, key=expenses_by_category.get, reverse=True
        )
        values = [expenses_by_category[c] for c in categories]
        ax_category.barh(categories[::-1], values[::-1], color=BLUE)
        style_axis(ax_category, "Expenses by category")
        ax_category.set_xlabel("Amount (€)", fontsize=8, color=MUTED)
    else:
        show_empty(ax_category, "Expenses by category")

    # Chart 3: income vs expenses.
    ax_comparison.clear()
    if finance.transactions:
        ax_comparison.bar(
            ["Income", "Expenses"], [income, expenses],
            color=[GREEN, RED], width=0.55
        )
        style_axis(ax_comparison, "Income vs expenses")
        ax_comparison.set_ylabel("Amount (€)", fontsize=8, color=MUTED)
    else:
        show_empty(ax_comparison, "Income vs expenses")

    # Chart 4: largest individual expenses.
    ax_top.clear()
    if expense_transactions:
        largest = sorted(
            expense_transactions, key=lambda t: t.amount, reverse=True
        )[:5]
        labels = [t.title[:20] for t in largest]
        values = [t.amount for t in largest]
        ax_top.barh(labels[::-1], values[::-1], color="#6B8EC7")
        style_axis(ax_top, "Largest individual expenses")
        ax_top.set_xlabel("Amount (€)", fontsize=8, color=MUTED)
    else:
        show_empty(ax_top, "Largest individual expenses")

    figure.tight_layout(pad=2.2)
    figure_canvas.draw_idle()


# ======================================================================
#                         TRANSACTIONS PAGE
# ======================================================================

transactions_header = page_header(
    transactions_page,
    "Transactions",
    "Add, edit and delete your income and expenses."
)

# ---- Filters ----
filters = tk.Frame(transactions_page, bg=BACKGROUND)
filters.pack(fill="x", padx=25, pady=(0, 10))

tk.Label(
    filters, text="Search", bg=BACKGROUND, fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(side="left")

search_var = tk.StringVar()
tk.Entry(
    filters, textvariable=search_var, font=("Segoe UI", 11),
    relief="solid", bd=1, width=26
).pack(side="left", padx=(8, 18), ipady=4)

tk.Label(
    filters, text="Type", bg=BACKGROUND, fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(side="left")

type_filter_var = tk.StringVar(value="All")
ttk.Combobox(
    filters, textvariable=type_filter_var,
    values=("All", "Income", "Expense"),
    state="readonly", width=10, font=("Segoe UI", 10)
).pack(side="left", padx=(8, 18))

tk.Label(
    filters, text="Category", bg=BACKGROUND, fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(side="left")

category_filter_var = tk.StringVar(value="All")
ttk.Combobox(
    filters, textvariable=category_filter_var,
    values=("All",) + CATEGORIES,
    state="readonly", width=14, font=("Segoe UI", 10)
).pack(side="left", padx=8)

count_label = tk.Label(
    filters, text="", bg=BACKGROUND, fg=MUTED, font=("Segoe UI", 10)
)
count_label.pack(side="right")

# ---- Action buttons (packed before the table so they never get squeezed) ----
actions = tk.Frame(transactions_page, bg=BACKGROUND)
actions.pack(side="bottom", fill="x", padx=25, pady=16)

# ---- Table with scrollbar ----
table_frame = tk.Frame(transactions_page, bg=BACKGROUND)
table_frame.pack(fill="both", expand=True, padx=25)

all_table = ttk.Treeview(
    table_frame, columns=columns, show="headings", selectmode="browse"
)
table_scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical", command=all_table.yview
)
all_table.configure(yscrollcommand=table_scrollbar.set)
setup_table_columns(all_table)

all_table.pack(side="left", fill="both", expand=True)
table_scrollbar.pack(side="right", fill="y")


def refresh_transactions(*_):
    for row in all_table.get_children():
        all_table.delete(row)

    search = search_var.get().strip().lower()
    wanted_type = type_filter_var.get().lower()
    wanted_category = category_filter_var.get()

    ordered = sorted(
        enumerate(finance.transactions),
        key=lambda pair: get_transaction_date(pair[1]),
        reverse=True
    )

    shown = 0
    for index, transaction in ordered:
        if wanted_type != "all" and \
                transaction.transaction_type.lower() != wanted_type:
            continue

        if wanted_category != "All" and transaction.category != wanted_category:
            continue

        if search and search not in transaction.title.lower() \
                and search not in transaction.category.lower():
            continue

        all_table.insert(
            "", "end",
            iid=str(index),   # position in finance.transactions
            values=transaction_row_values(transaction),
            tags=(transaction.transaction_type.lower(),)
        )
        shown += 1

    count_label.config(
        text=f"Showing {shown} of {len(finance.transactions)}"
    )

# report_header=page_header(
#        reports_page,
#        "Financial reports",
#         "Track your income, expenses and spending habits"
# )


def refresh_everything():
    refresh_dashboard()
    refresh_transactions()


search_var.trace_add("write", refresh_transactions)
type_filter_var.trace_add("write", refresh_transactions)
category_filter_var.trace_add("write", refresh_transactions)


def get_selected_index():
    selected = all_table.selection()
    if not selected:
        messagebox.showinfo(
            "No selection",
            "Click a transaction in the table first.",
            parent=root
        )
        return None
    return int(selected[0])


def delete_selected_transaction(event=None):
    index = get_selected_index()
    if index is None:
        return

    transaction = finance.transactions[index]

    confirmed = messagebox.askyesno(
        "Delete transaction",
        f"Delete this transaction?\n\n"
        f"{transaction.title}  ({format_money(transaction.amount)})",
        parent=root
    )
    if not confirmed:
        return

    removed = finance.transactions.pop(index)

    try:
        save_transaction(finance.transactions)
    except (OSError, TypeError, ValueError) as error:
        finance.transactions.insert(index, removed)   # roll back
        messagebox.showerror(
            "Delete failed",
            f"The transaction could not be deleted.\n\n{error}",
            parent=root
        )
        return

    refresh_everything()


def edit_selected_transaction(event=None):
    index = get_selected_index()
    if index is not None:
        open_transaction_form(index)


# ======================================================================
#                 ADD / EDIT TRANSACTION WINDOW
# ======================================================================

def open_transaction_form(index=None):
    """Open the form. Pass an index to edit an existing transaction."""
    editing = index is not None
    existing = finance.transactions[index] if editing else None

    form = tk.Toplevel(root)
    form.title(
        "Edit Transaction - SpendWise" if editing
        else "Add Transaction - SpendWise"
    )
    form.geometry("440x540")
    form.resizable(False, False)
    form.configure(bg=BACKGROUND)
    form.transient(root)
    form.grab_set()

    tk.Label(
        form,
        text="Edit Transaction" if editing else "Add a Transaction",
        bg=BACKGROUND, fg=NAVY, font=("Segoe UI", 19, "bold")
    ).pack(anchor="w", padx=28, pady=(24, 4))

    tk.Label(
        form, text="Enter the details below.",
        bg=BACKGROUND, fg=MUTED, font=("Segoe UI", 10)
    ).pack(anchor="w", padx=28, pady=(0, 16))

    fields = tk.Frame(form, bg=BACKGROUND)
    fields.pack(fill="x", padx=28)
    fields.grid_columnconfigure(1, weight=1)

    def add_field(label_text, row):
        tk.Label(
            fields, text=label_text, bg=BACKGROUND, fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(row=row, column=0, sticky="w", pady=7)

    def make_entry(row, initial=""):
        entry = tk.Entry(
            fields, font=("Segoe UI", 11), relief="solid", bd=1
        )
        entry.grid(row=row, column=1, sticky="ew", pady=7, ipady=5)
        if initial:
            entry.insert(0, initial)
        return entry

    add_field("Description", 0)
    title_entry = make_entry(0, existing.title if editing else "")

    add_field("Amount (€)", 1)
    amount_entry = make_entry(1, str(existing.amount) if editing else "")

    add_field("Category", 2)
    category_var = tk.StringVar(
        value=existing.category if editing else "Food"
    )
    ttk.Combobox(
        fields, textvariable=category_var, values=CATEGORIES,
        state="readonly", font=("Segoe UI", 11)
    ).grid(row=2, column=1, sticky="ew", pady=7, ipady=3)

    add_field("Type", 3)
    type_var = tk.StringVar(
        value=existing.transaction_type if editing else "expense"
    )
    ttk.Combobox(
        fields, textvariable=type_var, values=("expense", "income"),
        state="readonly", font=("Segoe UI", 11)
    ).grid(row=3, column=1, sticky="ew", pady=7, ipady=3)

    add_field("Date (YYYY-MM-DD)", 4)
    date_entry = make_entry(
        4,
        existing.transaction_date if editing else date.today().isoformat()
    )

    tk.Label(
        form,
        text="Use a category such as Food, Transport, Salary or Rent.",
        bg=BACKGROUND, fg=MUTED, wraplength=370, justify="left",
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=28, pady=(8, 0))

    def save_transaction_form():
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
        except ValueError as error:
            messagebox.showerror(
                "Check your entries",
                f"Please check the amount, date and transaction details."
                f"\n\n{error}",
                parent=form
            )
            return

        # Apply the change, then save. Roll back if saving fails.
        if editing:
            previous = finance.transactions[index]
            finance.transactions[index] = transaction
        else:
            finance.add_transaction(transaction)

        try:
            save_transaction(finance.transactions)
        except (OSError, TypeError, ValueError) as error:
            if editing:
                finance.transactions[index] = previous
            else:
                finance.transactions.pop()
            messagebox.showerror(
                "Save failed",
                f"The transaction could not be saved.\n\n{error}",
                parent=form
            )
            return

        refresh_everything()
        form.destroy()

    buttons = tk.Frame(form, bg=BACKGROUND)
    buttons.pack(fill="x", padx=28, pady=22)

    make_button(
        buttons,
        "Save Changes" if editing else "Save Transaction",
        save_transaction_form
    ).pack(side="left")

    make_button(
        buttons, "Cancel", form.destroy, primary=False
    ).pack(side="right")

    title_entry.focus_set()


def open_form():
    try:
        open_transaction_form()
    except Exception as error:
        messagebox.showerror(
            "Form error",
            f"{type(error).__name__}: {error}",
            parent=root
        )
        raise


# ---- Buttons that need the functions above ----


make_button(
    transactions_header, "+ Add Transaction", open_form
).pack(side="right", padx=(12, 0))

make_button(
    actions, "Edit Selected", edit_selected_transaction
).pack(side="left")

make_button(
    actions, "Delete Selected", delete_selected_transaction, primary=False
).pack(side="left", padx=(10, 0))

all_table.bind("<Delete>", delete_selected_transaction)
all_table.bind("<Double-1>", edit_selected_transaction)

report_header=page_header(
       reports_page,
       "Financial reports",
        "Track your income, expenses and spending habits"
)
report_filters=tk.Frame(
    reports_page,
    bg=BACKGROUND
)
report_filters.pack(
    fill="x",
    padx=28,
    pady=(0, 15)
)
tk.Label(
    report_filters,
    text="month",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Segoe UI", 11,"bold")
).pack(side="left")

month_var=tk.StringVar(value=date.today().strftime("%B"))
month_filter=ttk.Combobox(
    report_filters,
    textvariable=month_var,
    values=(
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ),
    state="readonly",
    width=15
)
month_filter.pack(side="left", padx=(10,20))
tk.Label(
    report_filters,
    text="Year",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
).pack(side="left")

year_var = tk.StringVar(value=str(date.today().year))

year_filter = ttk.Combobox(
    report_filters,
    textvariable=year_var,
    values=[str(year) for year in range(2020, 2036)],
    state="readonly",
    width=10
)

year_filter.pack(side="left", padx=(10, 20))
# -------------------- START --------------------

show_page("dashboard")
refresh_everything()
root.mainloop()