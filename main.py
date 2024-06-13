from fastapi import FastAPI, Depends, status
from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)


@app.post("/departments/", status_code=status.HTTP_201_CREATED)
async def post_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    crud.create_department(db, department)
    return JSONResponse(content={"message": "department created successfully"})


@app.post("/departments/batch/")
async def batch_departments(departments: List[schemas.Department], db: Session = Depends(get_db)):
    crud.batch_insert_departments(db, departments)
    return JSONResponse(content={"message": "departments created successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/departments/")
async def get_departments(db: Session = Depends(get_db)):
    all_departments = db.query(models.Departments).all()
    return all_departments


@app.post("/jobs/", status_code=status.HTTP_201_CREATED)
async def post_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    crud.create_job(db, job)
    return JSONResponse(content={"message": "job created successfully"})


@app.post("/jobs/batch/")
async def batch_jobs(jobs: List[schemas.Job], db: Session = Depends(get_db)):
    crud.batch_insert_jobs(db, jobs)
    return JSONResponse(content={"message": "jobs inserted successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/jobs/")
async def get_jobs(db: Session = Depends(get_db)):
    all_jobs = db.query(models.Jobs).all()
    return all_jobs


@app.post("/employees/", status_code=status.HTTP_201_CREATED)
async def post_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    crud.create_employee(db, employee)
    return JSONResponse(content={"message": "employee created successfully"})


@app.post("/employees/batch/")
async def batch_employees(employees: List[schemas.Employee], db: Session = Depends(get_db)):
    crud.batch_insert_employees(db, employees)
    return JSONResponse(content={"message": "employees inserted successfully"},
                        status_code=status.HTTP_201_CREATED)


@app.get("/employees/")
async def get_employees(db: Session = Depends(get_db)):
    all_employees = db.query(models.HiredEmployee).all()
    return all_employees
