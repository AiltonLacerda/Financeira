
# AI assistance disclosure:
# I used ChatGPT (OpenAI) as a learning and debugging aid during development.
# I discussed Flask routes, SQLite queries, authentication, error diagnosis,
# and interface improvements. I reviewed, adapted, and tested the resulting
# implementation and am responsible for the final project.

from flask import Flask, render_template, request, redirect, session
import os
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("A variável SECRET_KEY não foi configurada.")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

def get_db_connection():
    connection = sqlite3.connect("financeira.db")
    connection.row_factory = sqlite3.Row
    return connection

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")

        return view(*args, **kwargs)

    return wrapped_view

def format_currency(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

app.jinja_env.filters["currency"] = format_currency

@app.route("/")
@login_required
def index():

    connection = get_db_connection()

    transaction_type = request.args.get("type", "")
    category = request.args.get("category", "")

    query = "SELECT * FROM transactions WHERE user_id = ?"
    parameters = [session["user_id"]]

    if transaction_type:
        query += " AND type = ?"
        parameters.append(transaction_type)

    if category:
        query += " AND category = ?"
        parameters.append(category)

    query += " ORDER BY date DESC"

    transactions = connection.execute(
        query,
        parameters
    ).fetchall()

    total_receitas = connection.execute(
    """
    SELECT SUM(amount)
    FROM transactions
    WHERE type = 'receita'
    AND user_id = ?
    """,
    (session["user_id"],)
    ).fetchone()[0]

    total_despesas = connection.execute(
        """
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'despesa'
        AND user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    categories = [
        row["category"]
        for row in connection.execute(
            "SELECT DISTINCT category FROM transactions WHERE user_id = ? ORDER BY category",
            (session["user_id"],)
        ).fetchall()
    ]
    expenses_by_category = [
    dict(row)
    for row in connection.execute(
        """
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE type = 'despesa'
        AND user_id = ?
        GROUP BY category
        ORDER BY total DESC
        """,
        (session["user_id"],)
    ).fetchall()
    ]       

    connection.close()

    total_receitas = total_receitas or 0
    total_despesas = total_despesas or 0

    saldo = total_receitas - total_despesas

    return render_template(
        "index.html",
        transactions=transactions,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        categories=categories,
        expenses_by_category=expenses_by_category
    )

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        type = request.form["type"]
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        date = request.form["date"]

        allowed_types = ["receita", "despesa"]

        allowed_categories = [
            "Alimentação",
            "Moradia",
            "Transporte",
            "Saúde",
            "Educação",
            "Lazer",
            "Salário",
            "Investimentos",
            "Outros"
        ]

        try:
            amount = float(amount)
        except ValueError:
            return "Valor inválido", 400

        if type not in allowed_types:
            return "Tipo de lançamento inválido", 400

        if amount <= 0:
            return "O valor deve ser maior que zero", 400

        if category not in allowed_categories:
            return "Categoria inválida", 400

        if not date:
            return "A data é obrigatória", 400

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO transactions
            (user_id, type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                type,
                amount,
                category,
                description,
                date
            )
        )

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    connection = get_db_connection()
    connection.execute(
        """
        DELETE FROM transactions
        WHERE id = ?
        AND user_id = ?
        """,
        (id, session["user_id"])
    )
    connection.commit()
    connection.close()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    connection = get_db_connection()

    transaction = connection.execute(
        """
        SELECT *
        FROM transactions
        WHERE id = ?
        AND user_id = ?
        """,
        (id, session["user_id"])
    ).fetchone()

    if transaction is None:
        connection.close()
        return "Lançamento não encontrado", 404

    if request.method == "POST":
        type = request.form["type"]
        amount = request.form["amount"]
        category = request.form["category"]
        description = request.form["description"]
        date = request.form["date"]

        allowed_types = ["receita", "despesa"]
        allowed_categories = [
            "Alimentação",
            "Moradia",
            "Transporte",
            "Saúde",
            "Educação",
            "Lazer",
            "Salário",
            "Investimentos",
            "Outros"
        ]

        try:
            amount = float(amount)
        except ValueError:
            connection.close()
            return "Valor inválido", 400

        if type not in allowed_types:
            connection.close()
            return "Tipo de lançamento inválido", 400

        if amount <= 0:
            connection.close()
            return "O valor deve ser maior que zero", 400

        if category not in allowed_categories:
            connection.close()
            return "Categoria inválida", 400

        if not date:
            connection.close()
            return "A data é obrigatória", 400

        connection.execute(
            """
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, description = ?, date = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (
                type,
                amount,
                category,
                description,
                date,
                id,
                session["user_id"]
            )
        )
        connection.commit()
        connection.close()
        return redirect("/")

    connection.close()
    return render_template(
        "edit.html",
        transaction=transaction
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return "Usuário e senha são obrigatórios", 400

        if len(password) < 6:
            return "A senha deve ter pelo menos 6 caracteres", 400

        password_hash = generate_password_hash(password)

        connection = get_db_connection()

        try:

            connection.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (username, password_hash)
            )

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return "Esse usuário já existe", 400

        connection.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        connection.close()

        if user is None or not check_password_hash(user["password"], password):
            return "Usuário ou senha inválidos", 400

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug_mode)