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
