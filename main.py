from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

departments = [
    {"id": 1, "name": "Công nghệ thông tin"},
    {"id": 2, "name": "Kinh tế đối ngoại"}
]

students = [
    {"id": 1, "full_name": "Nguyen Van A", "status": "ACTIVE", "department_id": 1},
    {"id": 2, "full_name": "Tran Thi B", "status": "INACTIVE", "department_id": 1},
    {"id": 3, "full_name": "Le Van C", "status": "ACTIVE", "department_id": 2}
]

courses = [
    {"id": 101, "name": "Lập trình Python", "status": "OPEN"},
    {"id": 102, "name": "Cơ sở dữ liệu", "status": "OPEN"},
    {"id": 103, "name": "Kỹ năng mềm", "status": "CLOSED"}
]

enrollments = [
    {"id": 1, "student_id": 1, "course_id": 101}  
]

enrollment_id_counter = 2

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def get_student_details(student_id: int):
    # 1. Tìm sinh viên theo student_id
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sinh viên với ID {student_id} không tồn tại."
        )
    
    dept = next((d for d in departments if d["id"] == student["department_id"]), None)
    
    student_enrollments = [e for e in enrollments if e["student_id"] == student_id]
    
    student_courses = []
    for enroll in student_enrollments:
        course = next((c for c in courses if c["id"] == enroll["course_id"]), None)
        if course:
            student_courses.append(course)
            
    return {
        "id": student["id"],
        "full_name": student["full_name"],
        "status": student["status"],
        "department": dept,
        "courses": student_courses
    }


@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate):
    global enrollment_id_counter
    
    student = next((s for s in students if s["id"] == payload.student_id), None)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sinh viên với ID {payload.student_id} không tồn tại."
        )
        
    if student["status"] != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ sinh viên có trạng thái ACTIVE mới được phép đăng ký khóa học."
        )
        
    course = next((c for c in courses if c["id"] == payload.course_id), None)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Khóa học với ID {payload.course_id} không tồn tại."
        )
        
    if course["status"] != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khóa học đã đóng (CLOSED), không thể đăng ký."
        )
        
    already_enrolled = any(
        e for e in enrollments 
        if e["student_id"] == payload.student_id and e["course_id"] == payload.course_id
    )
    if already_enrolled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sinh viên đã đăng ký khóa học này trước đó."
        )
        
    new_enrollment = {
        "id": enrollment_id_counter,
        "student_id": payload.student_id,
        "course_id": payload.course_id
    }
    
    enrollments.append(new_enrollment)
    enrollment_id_counter += 1 
    
    return {
        "message": "Đăng ký khóa học thành công!",
        "enrollment": new_enrollment
    }