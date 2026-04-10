from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import random
from faker import Faker
from datetime import datetime

PROGRAMS = [
    ("BSMetE", "Bachelor of Science in Metallurgical Engineering", "COE"),
    ("BS-EMET", "Bachelor of Science in Environmental Engineering Technology", "COE"),
    ("BSIAM", "Bachelor of Science in Industrial Automation & Mechatronics", "COE"),
    ("BSETM", "Bachelor of Science in Engineering Technology Management", "COE"),

    ("BSBio-Bot", "Bachelor of Science in Biology (Botany)", "CSM"),
    ("BSBio-Zoo", "Bachelor of Science in Biology (Zoology)", "CSM"),
    ("BSBio-Mar", "Bachelor of Science in Biology (Marine)", "CSM"),
    ("BSBio-Gen", "Bachelor of Science in Biology (General)", "CSM"),
    ("BSChem", "Bachelor of Science in Chemistry", "CSM"),
    ("BSMath", "Bachelor of Science in Mathematics", "CSM"),
    ("BSPhys", "Bachelor of Science in Physics", "CSM"),
    ("BSStat", "Bachelor of Science in Statistics", "CSM"),

    ("BSPsych", "Bachelor of Science in Psychology", "CASS"),
    ("BA-ENG", "Bachelor of Arts in English", "CASS"),
    ("BA-FIL", "Bachelor of Arts in Filipino", "CASS"),
    ("BA-HIS", "Bachelor of Arts in History", "CASS"),
    ("BA-POLSCI", "Bachelor of Arts in Political Science", "CASS"),

    ("BSA", "Bachelor of Science in Accountancy", "CEBA"),
    ("BSBA-BE", "Bachelor of Science in Business Administration - Business Economics", "CEBA"),
    ("BSBA-Econ", "Bachelor of Science in Business Administration - Economics", "CEBA"),
    ("BSBA-EM", "Bachelor of Science in Business Administration - Entrepreneurial Marketing", "CEBA"),
    ("BSHRM", "Bachelor of Science in Hotel and Restaurant Management", "CEBA"),

    ("BSEd-Bio", "Bachelor of Secondary Education (Biology)", "CED"),
    ("BSEd-Chem", "Bachelor of Secondary Education (Chemistry)", "CED"),
    ("BSEd-Phys", "Bachelor of Secondary Education (Physics)", "CED"),
    ("BSEd-Math", "Bachelor of Secondary Education (Mathematics)", "CED"),
    ("BSEd-MAPEH", "Bachelor of Secondary Education (MAPEH)", "CED"),
    ("BSEd-TLE", "Bachelor of Secondary Education (TLE)", "CED"),
    ("BEEd-Eng", "Bachelor of Elementary Education (English)", "CED"),

    ("BSN", "Bachelor of Science in Nursing", "CHS"),
    ("BSCA", "Bachelor of Science in Computer Applications", "CCS"),
]

def seed_programs():
    db = QSqlDatabase.database()
    db.transaction()

    values = []

    for code, name, college in PROGRAMS:
        name = name.replace("'", "''")  # escape quotes
        values.append(f"('{code}', '{name}', '{college}')")

    sql = f"""
    INSERT INTO program (code, name, college)
    VALUES
    {",\n".join(values)}
    """

    query = QSqlQuery()

    if not query.exec(sql):
        print("Insert Error:", query.lastError().text())
        db.rollback()
    else:
        db.commit()
        print(f"Inserted {len(PROGRAMS)} programs successfully")
