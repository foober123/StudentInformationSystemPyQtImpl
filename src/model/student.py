from PyQt5.QtSql import QSqlQuery, QSqlDatabase

class StudentModel:
    @staticmethod
    def get_all(limit, offset, field=None, text=None, sort=None, order="ASC"):
        sql = """
            SELECT 
                s.id,
                s.firstname,
                s.lastname,
                COALESCE(p.name, 'Not Found') AS program,
                COALESCE(c.name, 'Not Found') AS college,
                s.year,
                s.gender
            FROM student s
            LEFT JOIN program p ON s.course = p.code
            LEFT JOIN college c ON p.college = c.code
        """

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
    def add(student):
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO student (id, firstname, lastname, course, year, gender)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(student["id"])
        query.addBindValue(student["firstname"])
        query.addBindValue(student["lastname"])
        query.addBindValue(student["course"])
        query.addBindValue(student["year"])
        query.addBindValue(student["gender"])
        return query.exec()

    @staticmethod
    def update(data):
        query = QSqlQuery()

        fields = []
        values = []

        for key in ["firstname", "lastname", "course", "year", "gender"]:
            if key in data:
                fields.append(f"{key} = ?")
                values.append(data[key])

        if not fields:
            print("No fields to update")
            return False

        sql = f"""
            UPDATE student
            SET {', '.join(fields)}
            WHERE id = ?
            """

        query.prepare(sql)

        for value in values:
            query.addBindValue(value)

        query.addBindValue(data["id"])

        if not query.exec():
            print("SQL Error (UPDATE):", query.lastError().text())
            return False

        return True

    @staticmethod
    def delete(code):
        query = QSqlQuery()
        query.prepare("DELETE FROM student WHERE id = ?")
        query.addBindValue(code)
       
        if not query.exec():
            print("SQL Error (DELETE):", query.lastError().text())
            return False

        QSqlDatabase.database().commit()
        return True


