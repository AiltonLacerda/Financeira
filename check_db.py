import sqlite3


connection = sqlite3.connect("financeira.db")

transactions = connection.execute(
    "SELECT * FROM transactions"
).fetchall()

for transaction in transactions:
    print(transaction)

connection.close()