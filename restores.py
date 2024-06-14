from sqlalchemy.orm import Session
import models
import avro.schema
from avro.datafile import DataFileReader
from avro.io import DatumReader
import os

job_schema = avro.schema.parse(open('backup/schemas/job.avsc').read())
department_schema = avro.schema.parse(open('backup/schemas/department.avsc').read())
employee_schema = avro.schema.parse(open('backup/schemas/employee.avsc').read())


def restore_employee_table(db: Session):
    avro_file = os.path.join(os.getcwd(), 'backup/employees.avro')
    result = 1
    if os.path.exists(avro_file):
        reader = DataFileReader(open('backup/employees.avro', 'rb'), DatumReader())
        for user in reader:
            db.add(models.HiredEmployee(**user))
            db.commit()
        reader.close()
        result = 0
    return result


def restore_job_table(db: Session):
    avro_file = os.path.join(os.getcwd(), 'backup/jobs.avro')
    result = 1
    if os.path.exists(avro_file):
        reader = DataFileReader(open('backup/jobs.avro', 'rb'), DatumReader())
        for job in reader:
            db.add(models.Jobs(**job))
            db.commit()
        reader.close()
        result = 0
    return result


def restore_department_table(db: Session):
    avro_file = os.path.join(os.getcwd(), 'backup/departments.avro')
    result = 1
    if os.path.exists(avro_file):
        reader = DataFileReader(open('backup/departments.avro', 'rb'), DatumReader())
        for department in reader:
            db.add(models.Departments(**department))
            db.commit()
        reader.close()
        result = 0
    return result
