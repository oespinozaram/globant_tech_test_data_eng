from pydantic import BaseModel


class Department(BaseModel):
    id: int
    department: str


class DepartmentCreate(BaseModel):
    department: str


class Job(BaseModel):
    id: int
    job: str


class JobCreate(BaseModel):
    pass


class HiredEmployee(BaseModel):
    id: int
    name: str
    datatime: str
    department: list[Department]
    job: list[Job]

    class Config:
        from_attributes = True
