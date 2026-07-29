from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): pass


class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    head_of_dept: Mapped[str] = mapped_column(String(100))
    budget: Mapped[float] = mapped_column(Numeric(12, 2))
    courses: Mapped[list['Course']] = relationship(back_populates='department')
    students: Mapped[list['Student']] = relationship(back_populates='department')


class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    code: Mapped[str] = mapped_column(String(20), unique=True)
    credits: Mapped[int] = mapped_column(Integer)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    department: Mapped[Department] = relationship(back_populates='courses')
    enrollments: Mapped[list['Enrollment']] = relationship(back_populates='course', cascade='all, delete-orphan')


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    enrollment_year: Mapped[int] = mapped_column(Integer)
    department: Mapped[Department] = relationship(back_populates='students')
    enrollments: Mapped[list['Enrollment']] = relationship(back_populates='student', cascade='all, delete-orphan')


class Enrollment(Base):
    __tablename__ = 'enrollments'
    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    enrollment_date: Mapped[date] = mapped_column(Date, default=date.today)
    grade: Mapped[str | None] = mapped_column(String(5), nullable=True)
    student: Mapped[Student] = relationship(back_populates='enrollments')
    course: Mapped[Course] = relationship(back_populates='enrollments')
