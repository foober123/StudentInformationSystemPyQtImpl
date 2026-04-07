from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import os

def init_schema():
    base_dir = os.path.dirname(__file__)  # folder of db.py
    schema_path = os.path.join(base_dir, "schema.sql")

    with open(schema_path, "r") as f:
        sql = f.read()

    query = QSqlQuery()

    for statement in sql.split(";"):
        if statement.strip():
            if not query.exec(statement):
                print("SQL Error:", query.lastError().text())


def connect_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("school.db")

    if not db.open():
        raise Exception("Database failed to open")

    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON;")

    init_schema()

    return db
