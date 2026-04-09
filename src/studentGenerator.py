from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import random
from faker import Faker
from datetime import datetime

fake = Faker()

PROGRAMS = ["BSCS", "BSIT", "BSBA"]
GENDERS = ["Male", "Female", "Other"]

def generate_student_id(year, index):
    return f"{year}-{index:04d}"

def seed_students(count=10000):
    db = QSqlDatabase.database()
    db.transaction()

    current_year = datetime.now().year
    values = []

    for i in range(1, count + 1):
        year_prefix = random.randint(current_year - 5, current_year)

        student_id = generate_student_id(year_prefix, i)
        firstname = fake.first_name().replace("'", "''")
        lastname = fake.last_name().replace("'", "''")
        course = random.choice(PROGRAMS)
        year = random.randint(1, 5)
        gender = random.choice(GENDERS)

        values.append(
            f"('{student_id}', '{firstname}', '{lastname}', '{course}', {year}, '{gender}')"
        )

    sql = f"""
    INSERT INTO student (id, firstname, lastname, course, year, gender)
    VALUES
    {",\n".join(values)}
    """

    query = QSqlQuery()

    if not query.exec(sql):
        print("Insert Error:", query.lastError().text())
        db.rollback()  # ❌ rollback on failure
    else:
        db.commit()  # ✅ commit if success
        print(f"Inserted {count} students successfully")
