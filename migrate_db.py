import sqlite3


connection = sqlite3.connect("financeira.db")


connection.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """
)


columns = connection.execute(
    "PRAGMA table_info(transactions)"
).fetchall()

column_names = [column[1] for column in columns]


if "user_id" not in column_names:

    connection.execute(
        "ALTER TABLE transactions ADD COLUMN user_id INTEGER"
    )


connection.commit()
connection.close()


print("Banco de dados atualizado com sucesso!")