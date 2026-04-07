from service.studentService import StudentService

def add_student(ctx):
    return StudentService.create_student(ctx["data"])

def list_student(ctx):
    query = StudentService.get_all_students()

    while query.next():
        print(
            query.value("id"),
            query.value("firstname"),
            query.value("lastname"),
            query.value("program"),
            query.value("college")
        )

    return

def remove_student(ctx):
    return StudentService.delete_student(ctx["id"])

def update_student(ctx):
    return StudentService.update_student(ctx["id"], ctx["data"])
