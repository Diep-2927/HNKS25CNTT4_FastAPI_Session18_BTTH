from fastapi import FastAPI
from database import engine
from app.models import department as model_department
from app.models import student as model_student
from app.models import course as model_course
from app.models import enrollment as model_enrollment

from app.routers import school as router_school

model_department.Base.metadata.create_all(bind=engine)
model_student.Base.metadata.create_all(bind=engine)
model_course.Base.metadata.create_all(bind=engine)
model_enrollment.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Training Center Management")

app.include_router(router_school.router)

@app.get("/")
def root():
    return {"message": "Hệ thống quản lý trung tâm đào tạo sẵn sàng!"}