from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel): model_config = ConfigDict(from_attributes=True)
class CourseCreate(BaseModel):
    name: str = Field(min_length=1); code: str = Field(min_length=1); credits: int = Field(gt=0); department_id: int = Field(gt=0)
class CourseUpdate(BaseModel):
    name: str | None = None; code: str | None = None; credits: int | None = Field(default=None, gt=0); department_id: int | None = Field(default=None, gt=0)
class CourseResponse(ORMModel):
    id: int; name: str; code: str; credits: int; department_id: int
class StudentCreate(BaseModel):
    first_name: str = Field(min_length=1); last_name: str = Field(min_length=1); email: EmailStr; department_id: int = Field(gt=0); enrollment_year: int = Field(gt=0)
class StudentUpdate(BaseModel):
    first_name: str | None = None; last_name: str | None = None; email: EmailStr | None = None; department_id: int | None = Field(default=None, gt=0); enrollment_year: int | None = Field(default=None, gt=0)
class StudentResponse(ORMModel):
    id: int; first_name: str; last_name: str; email: EmailStr; department_id: int; enrollment_year: int
class EnrollmentCreate(BaseModel):
    student_id: int = Field(gt=0); course_id: int = Field(gt=0); enrollment_date: date | None = None; grade: str | None = Field(default=None, max_length=5)
class EnrollmentUpdate(BaseModel):
    grade: str | None = Field(default=None, max_length=5)
class EnrollmentResponse(ORMModel):
    id: int; student_id: int; course_id: int; enrollment_date: date; grade: str | None
