from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Departments(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    departament = Column(String, nullable=False)


class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, nullable=False)


class HiredEmployee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    datatime = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)

    department = relationship(Departments, backref='hired_employees')
    job = relationship(Jobs, backref='hired_employees')
