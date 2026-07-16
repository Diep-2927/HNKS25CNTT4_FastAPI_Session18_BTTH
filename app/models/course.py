from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False) # OPEN, CLOSED

    enrollments = relationship("Enrollment", back_populates="course")