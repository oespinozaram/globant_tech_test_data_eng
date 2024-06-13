from sqlalchemy.orm import Session
import models
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter

job_schema = avro.schema.parse(open('backup/schemas/job.avsc').read())
department_schema = avro.schema.parse(open('backup/schemas/department.avsc').read())
employee_schema = avro.schema.parse(open('backup/schemas/employee.avsc').read())


def create_jobs_backup(db: Session):
    all_jobs = db.query(models.Jobs).all()
    writer = DataFileWriter(open("backup/jobs.avro", "wb"), DatumWriter(), job_schema)
    for job in all_jobs:
        writer.append({"id": job.id, "job": "{}".format(job.job)})
    writer.close()


def create_departments_backup(db: Session):
    all_departments = db.query(models.Departments).all()
    writer = DataFileWriter(open("backup/departments.avro", "wb"), DatumWriter(), department_schema)
    for department in all_departments:
        writer.append({"id": department.id, "department": '{}'.format(department.department)})
    writer.close()


def create_employees_backup(db: Session):
    all_employees = db.query(models.HiredEmployee).all()
    writer = DataFileWriter(open("backup/employees.avro", "wb"), DatumWriter(), employee_schema)
    for employee in all_employees:
        writer.append({u'id': employee.id, u'name': u'{}'.format(employee.name),
                       u'datetime': u'{}'.format(employee.datetime), u'department_id': employee.department_id,
                       u'job_id': employee.job_id})
    writer.close()
