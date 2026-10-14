import sqlite3


connection = sqlite3.connect("financeira.db")

with open("schema.sql") as file:
    connection.executescript(file.read())

connection.close()

print("Banco de dados criado com sucesso!")