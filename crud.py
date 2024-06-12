from sqlalchemy.orm import Session
import models
import schemas


def create_department(db: Session, department: schemas.DepartmentCreate):
    new_department = models.Departments(**department.dict())
    db.add(department)
    db.commit()
    db.refresh(department)
    return new_department
