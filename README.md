# Financeira

#### Video Demo: [https://youtu.be/UGRyntcXUdk]

## Description

Financeira is a web-based personal finance management application developed as my final project for CS50x: Introduction to Computer Science, offered by Harvard University.

The application helps users organize their personal finances by recording income and expenses, categorizing transactions, and monitoring their financial activity through a dashboard. I chose this project because personal financial organization is a practical problem, and I wanted to apply the programming concepts learned throughout CS50x to build a useful application.

Financeira was developed using Python, Flask, SQLite, HTML, CSS, and Jinja templates. It includes user authentication, transaction management, financial summaries, filtering tools, and data visualization.

## Features

### User Authentication

Users can create an account and log in with a username and password. Passwords are hashed using Werkzeug before being stored in the database. Flask sessions maintain the authenticated user's identity, and protected routes require authentication before users can access their financial information.

### Income and Expense Management

Users can register, edit, and delete financial transactions. Each transaction includes a type, amount, category, description, and date.

The application validates transaction types, categories, amounts, and required dates before saving changes to the database.

### Financial Dashboard

The dashboard displays total income, total expenses, and the resulting balance. It also presents a transaction history so users can review their financial activity.

### Filtering and Data Visualization

Users can filter transactions by type and category. A chart built with Chart.js visualizes expenses grouped by category, helping users understand how their spending is distributed.

### User Data Isolation

Each transaction is associated with a user account. Database queries restrict transaction lists, editing, deletion, and financial summaries to the authenticated user's records.

## Technologies Used

- **Python:** Backend logic and data processing.
- **Flask:** Web framework, routing, request handling, and sessions.
- **SQLite:** Relational database for user accounts and financial transactions.
- **HTML:** Structure of the application's pages.
- **CSS:** Styling and responsive interface design.
- **Jinja:** Dynamic HTML rendering through Flask templates.
- **Werkzeug:** Password hashing and password verification.
- **Chart.js:** Visualization of expenses by category.

## Project Structure

- `app.py`: Main application, routes, authentication, database queries, and transaction management.
- `schema.sql`: SQL commands for creating the transactions table.
- `init_db.py`: Initializes the database using the SQL schema.
- `migrate_db.py`: Creates the users table and adds the `user_id` column to transactions when necessary.
- `check_db.py`: Utility script for inspecting transaction records in the local database.
- `templates/`: HTML templates for the dashboard, login, registration, and transaction forms.
- `static/`: CSS styles and other static assets.
- `.gitignore`: Excludes local files, virtual environments, databases, and secrets from version control.

## Installation and Usage

### Requirements

Python 3 and pip must be installed on your computer.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Financeira
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of the repository.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install Flask
```

### 4. Initialize the database

Run the following commands in order:

```bash
python init_db.py
python migrate_db.py
```

These commands create the transactions table, the users table, and the user association column in a new local database.

**Important:** These initialization commands are intended for a fresh database. Do not run `init_db.py` over an existing database containing data, because the script attempts to create the transactions table again.

### 5. Configure the secret key

On Windows PowerShell, set a local secret key before starting the application:

```powershell
$env:SECRET_KEY = "replace-with-a-random-secret-key"
```

Use a strong, private value for your own environment. Never commit real secret keys to the repository.

### 6. Run the application

```bash
python app.py
```

Open the local address displayed in the terminal, typically `http://127.0.0.1:5000`.

Create an account to start recording income and expenses.

## Design Decisions

I chose Flask because it provides a straightforward way to build a web application using Python while learning about routing, HTTP requests, sessions, and templates. SQLite provides a lightweight relational database without requiring a separate database server.

I also implemented user-specific database queries so that each authenticated user can access only their own financial records. The project combines backend programming, database design, authentication, and interface development in a practical application.

## Future Improvements

Possible improvements include monthly reports, budget planning, recurring transactions, data export, and additional financial visualizations.

## Acknowledgments

This project was developed as the final project for CS50x: Introduction to Computer Science, offered by Harvard University.