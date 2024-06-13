from typing import List

from sqlalchemy.orm import Session
import models
import schemas


def create_department(db: Session, department: schemas.DepartmentCreate):
    new_department = models.Departments(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


def create_job(db: Session, job: schemas.JobCreate):
    new_job = models.Jobs(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    new_employee = models.HiredEmployee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def batch_insert_jobs(db: Session, jobs: List[schemas.Job]):
    job_list = []
    for count, job in enumerate(jobs, start=1):
        job_item = models.Jobs(**job.dict())
        job_list.append(job_item)
        if count == 1000:
            break
    db.bulk_save_objects(job_list)
    db.commit()


def batch_insert_employees(db: Session, employees: List[schemas.Employee]):
    employee_list = []
    for count, employee in enumerate(employees, start=1):
        employee_item = models.HiredEmployee(**employee.dict())
        employee_list.append(employee_item)
        if count == 1000:
            break
    db.bulk_save_objects(employee_list)
    db.commit()


def batch_insert_departments(db: Session, departments: List[schemas.Department]):
    department_list = []
    for count, department in enumerate(departments):
        department_item = models.Departments(**department.dict())
        department_list.append(department_item)
        if count == 1000:
            break
    db.bulk_save_objects(department_list)
    db.commit()
