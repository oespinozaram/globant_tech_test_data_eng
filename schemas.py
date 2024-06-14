from pydantic import BaseModel


class DepartmentBase(BaseModel):
    department: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class JobBase(BaseModel):
    job: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    name: str
    datetime: str
    department_id: int
    job_id: int


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
