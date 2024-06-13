CREATE TABLE departments (
    id INTEGER PRIMARY KEY NOT NULL,
    department VARCHAR
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY NOT NULL,
    job VARCHAR
);

CREATE TABLE hired_employees (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR,
    datetime VARCHAR,
    department_id INTEGER,
    job_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);