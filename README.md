# 💙 SpendWise — Personal Finance Tracker

**Take control of your money, one transaction at a time.**

SpendWise is a Python-based personal finance application designed to help users track their income and expenses, understand their spending habits, and monitor their financial balance. With a dashboard, visual spending insights, and persistent transaction storage, SpendWise aims to make personal financial management simpler and more accessible.

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Built With](#-built-with)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Roadmap](#-roadmap)
- [Learning Goals](#-learning-goals)
- [Contributing](#-contributing)
- [License](#-license)

## Overview

Managing personal finances can be challenging without a clear picture of where money comes from and where it goes.

SpendWise aims to address this by providing a desktop application for recording transactions, monitoring income and expenses, and visualizing financial activity. The long-term goal is to help users recognize spending patterns and make more informed financial decisions.

## Features

- **Income and expense tracking** — record financial transactions and organize them by category.
- **Transaction validation** — validate transaction details, including descriptions, amounts, categories, and transaction types.
- **Financial dashboard** — view key financial summaries, including income, expenses, and balance.
- **Visual insights** — use charts to explore financial activity and spending patterns.
- **Persistent storage** — save transactions locally in JSON format so they can be loaded again when the application starts.
- **Transaction history** — review recorded transactions and their details.
- **Automated tests** — test core financial calculations, transaction validation, and storage functionality.

## Built With

| Technology | Purpose |
|---|---|
| Python | Application logic and financial calculations |
| Tkinter | Desktop graphical user interface |
| Matplotlib | Financial charts and visualizations |
| JSON | Local transaction storage |
| Pytest | Automated testing |

##  Project Structure

```text
SpendWise/
├── app.py
├── main.py
├── finance.py
├── transaction.py
├── storage.py
├── requirements.txt
├── src/
│   └── spendwise/
│       └── __init__.py
├── tests/
│   ├── test_basic.py
│   ├── test_finance.py
│   ├── test_storage.py
│   └── test_transaction.py
├── test_tkinter.py
├── .gitignore
└── README.md
```

- `app.py` — desktop application interface and dashboard.
- `main.py` — additional application entry-point module.
- `finance.py` — financial calculations and transaction management.
- `transaction.py` — transaction model and input validation.
- `storage.py` — local JSON persistence.
- `tests/` — automated tests for core functionality.
- `requirements.txt` — Python package dependencies.


### Prerequisites

- Python 3.12 or a compatible Python version.
- Git.
- PyCharm or another Python development environment.

### 1. Clone the repository

```bash
git clone https://github.com/ashleyegbert/SpendWise.git
cd SpendWise
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the application

```powershell
python app.py
```

The SpendWise desktop application should open in a new window.

## Running Tests

To run the automated test suite, install pytest if it is not already included in your dependencies:

```powershell
python -m pip install pytest
```

Then run:

```powershell
python -m pytest
```

The tests cover important parts of the application, including financial calculations, transaction validation, and data storage.

##  Roadmap

SpendWise is an evolving project. Planned improvements include:

- [ ] Monthly financial reports and summaries.
- [ ] More detailed spending analysis.
- [ ] Personalized recommendations based on spending patterns.
- [ ] Budget setting and expense limits.
- [ ] Improved transaction management, including editing and deleting records.
- [ ] Additional charts and financial insights.
- [ ] Further improvements to usability and automated test coverage.

##  Learning Goals

SpendWise is also a practical software development and learning project. It provides an opportunity to develop skills in:

- Python programming and object-oriented design.
- GUI development with Tkinter.
- Financial data processing and validation.
- Data persistence using JSON.
- Data visualization with Matplotlib.
- Software testing and version control with Git and GitHub.

##  Contributing

Suggestions, bug reports, and ideas for improvement are welcome. If you would like to contribute, feel free to fork the repository and submit a pull request.

## License

No license has been selected yet. A license can be added when the project's sharing and reuse terms have been decided.

---

**SpendWise — Understand your spending. Make informed decisions.**
