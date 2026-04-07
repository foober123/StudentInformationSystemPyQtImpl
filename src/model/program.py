from PyQt5.QtSql import QSqlQuery, QSqlDatabase

class ProgramModel:
    @staticmethod
    def get_all(limit, offset, field=None, text=None, sort=None, order="ASC"):
        sql = """
        SELECT 
        p.code,
        p.name,
        COALESCE(c.code, 'Not Found') AS college
        FROM program p
        LEFT JOIN college c ON p.college = c.code
        """

        values = []

        if field and text:
            sql += f" WHERE {field} LIKE ?"
            values.append(f"%{text}%")


        if sort:
            sql += f" ORDER BY COALESCE({sort}, '') {order}"

        sql += " LIMIT ? OFFSET ?"
        values.extend([limit, offset])

        return sql, values

    @staticmethod
    def count(field=None, text=None):
        sql = """
            SELECT COUNT(*)
            FROM student s
            LEFT JOIN program p ON s.course = p.code
            LEFT JOIN college c ON p.college = c.code
        """

        values = []

        if field and text:
            sql += f" WHERE {field} LIKE ?"
            values.append(f"%{text}%")

        query = QSqlQuery()
        query.prepare(sql)

        for v in values:
            query.addBindValue(v)

        if not query.exec():
            print("SQL Error (COUNT - STUDENT):", query.lastError().text())
            return 0

        if query.next():
            return query.value(0)

        return 0


    @staticmethod
    def add(program):
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO program (code, name, college)
            VALUES (?, ?, ?)
        """)
        query.addBindValue(program["code"])
        query.addBindValue(program["name"])
        query.addBindValue(program["college"] or None)  # FK
        return query.exec()

    @staticmethod
    def delete(code):
        query = QSqlQuery()
        query.prepare("DELETE FROM program WHERE code = ?")
        query.addBindValue(code)
        
        if not query.exec():
            print("SQL Error (DELETE):", query.lastError().text())
            return False

        QSqlDatabase.database().commit()
        return True


    @staticmethod
    def update(program):
        query = QSqlQuery()
        query.prepare("""
            UPDATE program
            SET name = ?, college = ?
            WHERE code = ?
        """)

        query.addBindValue(program["name"])
        query.addBindValue(program["college"])  # can be None
        query.addBindValue(program["code"])

        if not query.exec():
            print("SQL Error (UPDATE):", query.lastError().text())
            return False

        return True

    @staticmethod
    def get_by_code(code):
        query = QSqlQuery()
        query.prepare("""
            SELECT code, name, college
            FROM program
            WHERE code = ?
        """)

        query.addBindValue(code)

        if not query.exec():
            print("SQL Error (GET BY CODE):", query.lastError().text())
            return None

        if query.next():
            return {
                "code": query.value(0),
                "name": query.value(1),
                "college": query.value(2)  # may be None
            }

        return None
