from pydantic import BaseModel
from typing import List

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class DepartmentBase(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    id: int
    name: str
    status: str
    class Config:
        from_attributes = True

class StudentDetailResponse(BaseModel):
 
    id: int
    full_name: str
    status: str
    department: DepartmentBase
    courses: List[CourseBase]

    class Config:
        from_attributes = True