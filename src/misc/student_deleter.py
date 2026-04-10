from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import random
from faker import Faker
from datetime import datetime


def delete_all_students():
    db = QSqlDatabase.database()
    db.transaction()

    query = QSqlQuery()

    sql = "DELETE FROM student"

    if not query.exec(sql):
        print("Delete Error:", query.lastError().text())
        db.rollback()
    else:
        db.commit()
        print("All students deleted successfully")
