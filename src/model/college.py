from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class CollegeModel:
    @staticmethod
    def get_all(limit, offset, field=None, text=None, sort=None, order="ASC"):
        sql = "SELECT code, name FROM college"

        values = []

        if field and text:
            sql += f" WHERE {field} LIKE ?"
            values.append(f"%{text}%")

        if sort:
            sql += f" ORDER BY {sort} {order}"

        sql += " LIMIT ? OFFSET ?"
        values.extend([limit, offset])

        return sql, values


    @staticmethod
    def count(field=None, text=None):
        sql = "SELECT COUNT(*) FROM college"

        values = []

        if field and text:
            sql += f" WHERE {field} LIKE ?"
            values.append(f"%{text}%")

        query = QSqlQuery()
        query.prepare(sql)

        for v in values:
            query.addBindValue(v)

        if not query.exec():
            print("SQL Error (COUNT - COLLEGE):", query.lastError().text())
            return 0

        if query.next():
            return query.value(0)

        return 0

    @staticmethod
    def add(college):
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO college (code, name)
            VALUES (?, ?)
        """)
        query.addBindValue(college["code"])
        query.addBindValue(college["name"])

        if not query.exec():
            print("SQL Error (ADD):", query.lastError().text())
            return False
        return True

    @staticmethod
    def delete(code):
        query = QSqlQuery()
        query.prepare("DELETE FROM college WHERE code = ?")
        query.addBindValue(code)

        if not query.exec():
            print("SQL Error (DELETE):", query.lastError().text())
            return False

        QSqlDatabase.database().commit()
        return True

    @staticmethod
    def update(data):
        query = QSqlQuery()
        query.prepare("""
            UPDATE college
            SET name = ?
            WHERE code = ?
        """)

        query.addBindValue(data["name"])
        query.addBindValue(data["code"])

        if not query.exec():
            print("SQL Error (UPDATE):", query.lastError().text())
            return False

        return True
