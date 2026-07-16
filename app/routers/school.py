from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas import school as schemas
from app.services import school as services

router = APIRouter(tags=["Training Center API"])

@router.get("/students/{student_id}", response_model=schemas.StudentDetailResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return services.get_student_details(db, student_id)

@router.post("/enrollments", status_code=status.HTTP_201_CREATED)
def enroll_student(data: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    enrollment = services.create_new_enrollment(db, data)
    return {"message": "Đăng ký thành công", "enrollment_id": enrollment.id}