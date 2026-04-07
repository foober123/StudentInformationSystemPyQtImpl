PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS college (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS program (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    college TEXT,  -- must be NULLABLE for SET NULL

    FOREIGN KEY (college)
        REFERENCES college(code)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS student (
    id TEXT PRIMARY KEY,  -- format: YYYY-NNNN
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    course TEXT,  -- must be NULLABLE for SET NULL
    year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 5),
    gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')),

    FOREIGN KEY (course)
        REFERENCES program(code)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_student_lastname
    ON student(lastname);

CREATE INDEX IF NOT EXISTS idx_student_firstname
    ON student(firstname);

CREATE INDEX IF NOT EXISTS idx_student_course
    ON student(course);

CREATE INDEX IF NOT EXISTS idx_program_college
    ON program(college);



