from fastapi import FastAPI, Depends, status, HTTPException
from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import crud
import models
import schemas
import backups
import restores
from database import SessionLocal, engine

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


@app.post("/departments/", tags=["Departments"])
async def post_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    crud.create_department(db, department)
    return JSONResponse(content={"message": "department created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.post("/departments/batch/", tags=["Departments"])
async def batch_departments(departments: List[schemas.Department], db: Session = Depends(get_db)):
    crud.batch_insert_departments(db, departments)
    return JSONResponse(content={"message": "departments created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/departments/", tags=["Departments"])
async def get_departments(db: Session = Depends(get_db)):
    all_departments = db.query(models.Departments).all()
    return all_departments


@app.post("/jobs/", tags=["Jobs"])
async def post_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    crud.create_job(db, job)
    return JSONResponse(content={"message": "job created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.post("/jobs/batch/", tags=["Jobs"])
async def batch_jobs(jobs: List[schemas.Job], db: Session = Depends(get_db)):
    crud.batch_insert_jobs(db, jobs)
    return JSONResponse(content={"message": "jobs inserted successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/jobs/", tags=["Jobs"])
async def get_jobs(db: Session = Depends(get_db)):
    all_jobs = db.query(models.Jobs).all()
    return all_jobs


@app.get("/jobs/backup/", tags=["Jobs"])
def backup_jobs(db: Session = Depends(get_db)):
    backups.create_jobs_backup(db)
    return JSONResponse(content={"message": "jobs backup created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/jobs/restore/", tags=["Jobs"])
def restore_jobs(db: Session = Depends(get_db)):
    if restores.restore_job_table(db) == 1:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={"message": "jobs table restored!"},
                        status_code=status.HTTP_200_OK)


@app.get("/departments/restore/", tags=["Departments"])
def restore_departments(db: Session = Depends(get_db)):
    if restores.restore_department_table(db) == 1:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={"message": "departments table restored!"},
                        status_code=status.HTTP_200_OK)


@app.get("/departments/backup/", tags=["Departments"])
def backup_departments(db: Session = Depends(get_db)):
    backups.create_departments_backup(db)
    return JSONResponse(content={"message": "departments backup created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/employees/backup/", tags=["Employees"])
def backup_employees(db: Session = Depends(get_db)):
    backups.create_employees_backup(db)
    return JSONResponse(content={"message": "employees backup created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/employees/restore/", tags=["Employees"])
def restore_employees(db: Session = Depends(get_db)):
    if restores.restore_employee_table(db) == 1:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={"message": "employees table restored!"},
                        status_code=status.HTTP_200_OK)


@app.post("/employees/", tags=["Employees"])
async def post_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    crud.create_employee(db, employee)
    return JSONResponse(content={"message": "employee created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.post("/employees/batch/", tags=["Employees"])
async def batch_employees(employees: List[schemas.Employee], db: Session = Depends(get_db)):
    crud.batch_insert_employees(db, employees)
    return JSONResponse(content={"message": "employees inserted successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/employees/", tags=["Employees"])
async def get_employees(db: Session = Depends(get_db)):
    all_employees = db.query(models.HiredEmployee).all()
    return all_employees
