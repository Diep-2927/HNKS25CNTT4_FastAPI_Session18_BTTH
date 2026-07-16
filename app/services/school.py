from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.student import Student
from app.models.department import Department
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.school import EnrollmentCreate

def get_student_details(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")

    enrolled_courses = [enrollment.course for enrollment in student.enrollments]

    return {
        "id": student.id,
        "full_name": student.full_name,
        "status": student.status,
        "department": student.department,
        "courses": enrolled_courses
    }

def create_new_enrollment(db: Session, data: EnrollmentCreate):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Sinh viên không ở trạng thái ACTIVE")

    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại")
    if course.status != "OPEN":
        raise HTTPException(status_code=400, detail="Khóa học đã đóng (CLOSED)")

    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký khóa học này rồi")

    new_enrollment = Enrollment(student_id=data.student_id, course_id=data.course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return new_enrollment