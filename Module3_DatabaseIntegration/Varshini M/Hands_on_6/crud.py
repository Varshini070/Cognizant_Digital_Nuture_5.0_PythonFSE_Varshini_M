"""
n+1 query comparison

Without using joinedload the query was executed for each record and fetched one by one, making the performance slower.

With joinedload records were fetched at once with a single execution instead of multiple times improving performance.
"""

from sqlalchemy.orm import sessionmaker
from models import *
from sqlalchemy.orm import joinedload

Session = sessionmaker(bind=engine)
session = Session()

d1 = Department(dept_name="Computer Science")
d2 = Department(dept_name="Electronics")
d3 = Department(dept_name="Mechanical")
session.add_all([d1,d2,d3])
session.commit()

s1 = Student(
    first_name="Arjun",
    last_name="Mehta",
    email="arjun@gmail.com",
    enrollment_year=2022,
    department=d1
)

s2 = Student(
    first_name="Priya",
    last_name="Suresh",
    email="priya@gmail.com",
    enrollment_year=2022,
    department=d1
)

s3 = Student(
    first_name="Rohan",
    last_name="Verma",
    email="rohan@gmail.com",
    enrollment_year=2021,
    department=d2
)

s4 = Student(
    first_name="Sneha",
    last_name="Patel",
    email="sneha@gmail.com",
    enrollment_year=2023,
    department=d3
)

s5 = Student(
    first_name="Deepika",
    last_name="Rao",
    email="deepika@gmail.com",
    enrollment_year=2022,
    department=d1
)
session.add_all([s1,s2,s3,s4,s5])
session.commit()

c1 = Course(course_name="DBMS", course_code="CS102", credits=3)
c2 = Course(course_name="DSA", course_code="CS101", credits=4)
c3 = Course(course_name="OOP", course_code="CS103", credits=4)
session.add_all([c1,c2,c3])
session.commit()

e1 = Enrollment(student=s1,course=c1)
e2 = Enrollment(student=s2,course=c2)
e3 = Enrollment(student=s3,course=c1)
e4 = Enrollment(student=s5,course=c3)
session.add_all([e1,e2,e3,e4])
session.commit()

students = (session.query(Student).join(Department).filter(Department.dept_name=="Computer Science").all())
for s in students:
    print(s.first_name,s.last_name)

enrollments = session.query(Enrollment).options(joinedload(Enrollment.student),joinedload(Enrollment.course)).all()
for e in enrollments:
    print(e.student.first_name,e.course.course_name)

student = session.query(Student).filter_by(email="arjun@gmail.com").first()
student.enrollment_year=2024
session.commit()

record=session.query(Enrollment).first()
session.delete(record)
session.commit()
