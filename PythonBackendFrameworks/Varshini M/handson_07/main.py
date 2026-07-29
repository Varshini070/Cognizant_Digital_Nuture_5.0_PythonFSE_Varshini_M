from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, get_db
from models import Base, Course, Department, Enrollment, Student
from schemas import (CourseCreate, CourseResponse, CourseUpdate, EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate, StudentCreate, StudentResponse, StudentUpdate)


async def require(model, item_id, db, label):
    item = await db.get(model, item_id)
    if item is None: raise HTTPException(404, f'{label} not found')
    return item

async def commit(db):
    try: await db.commit()
    except IntegrityError:
        await db.rollback(); raise HTTPException(409, 'Duplicate or invalid relationship')

def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection: await connection.run_sync(Base.metadata.create_all)
    async with SessionLocal() as db:
        if not (await db.execute(select(Department.id).limit(1))).scalar_one_or_none():
            db.add_all([Department(name='Engineering', head_of_dept='Anita Rao', budget=500000), Department(name='Science', head_of_dept='Rahul Mehta', budget=350000)])
            await db.commit()
    yield
    await engine.dispose()

app = FastAPI(title='Course Management API', description='Async course, student, and enrollment management API.', version='1.1', contact={'name': 'Course API Team', 'email': 'support@example.com'}, lifespan=lifespan)

@app.get('/', tags=['System'])
async def root(): return {'message': 'API running'}

@app.get('/api/courses/', response_model=list[CourseResponse], tags=['Courses'])
async def list_courses(db: AsyncSession = Depends(get_db)): return (await db.execute(select(Course))).scalars().all()

@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'], summary='Create a course', response_description='The newly created course')
async def create_course(data: CourseCreate, db: AsyncSession = Depends(get_db)):
    await require(Department, data.department_id, db, 'Department'); item = Course(**data.model_dump()); db.add(item); await commit(db); await db.refresh(item); return item

@app.get('/api/courses/{item_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(item_id: int, db: AsyncSession = Depends(get_db)): return await require(Course, item_id, db, 'Course')

@app.put('/api/courses/{item_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(item_id: int, data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    item = await require(Course, item_id, db, 'Course')
    if data.department_id: await require(Department, data.department_id, db, 'Department')
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    await commit(db); await db.refresh(item); return item

@app.delete('/api/courses/{item_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(item_id: int, db: AsyncSession = Depends(get_db)):
    await db.delete(await require(Course, item_id, db, 'Course')); await db.commit(); return Response(status_code=204)

@app.get('/api/courses/{item_id}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def course_students(item_id: int, db: AsyncSession = Depends(get_db)):
    await require(Course, item_id, db, 'Course'); return (await db.execute(select(Student).join(Enrollment).where(Enrollment.course_id == item_id))).scalars().all()

@app.get('/api/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)): return (await db.execute(select(Student))).scalars().all()
@app.post('/api/students/', response_model=StudentResponse, status_code=201, tags=['Students'])
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    await require(Department, data.department_id, db, 'Department'); item = Student(**data.model_dump()); db.add(item); await commit(db); await db.refresh(item); return item
@app.get('/api/students/{item_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(item_id: int, db: AsyncSession = Depends(get_db)): return await require(Student, item_id, db, 'Student')
@app.put('/api/students/{item_id}', response_model=StudentResponse, tags=['Students'])
async def update_student(item_id: int, data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    item = await require(Student, item_id, db, 'Student')
    if data.department_id: await require(Department, data.department_id, db, 'Department')
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    await commit(db); await db.refresh(item); return item
@app.delete('/api/students/{item_id}', status_code=204, tags=['Students'])
async def delete_student(item_id: int, db: AsyncSession = Depends(get_db)):
    await db.delete(await require(Student, item_id, db, 'Student')); await db.commit(); return Response(status_code=204)

@app.get('/api/enrollments/', response_model=list[EnrollmentResponse], tags=['Enrollments'])
async def list_enrollments(db: AsyncSession = Depends(get_db)): return (await db.execute(select(Enrollment))).scalars().all()
@app.post('/api/enrollments/', response_model=EnrollmentResponse, status_code=201, tags=['Enrollments'])
async def create_enrollment(data: EnrollmentCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    student = await require(Student, data.student_id, db, 'Student'); await require(Course, data.course_id, db, 'Course')
    item = Enrollment(**data.model_dump(exclude_none=True)); db.add(item); await commit(db); await db.refresh(item)
    background_tasks.add_task(send_confirmation_email, student.email); return item
@app.get('/api/enrollments/{item_id}', response_model=EnrollmentResponse, tags=['Enrollments'])
async def get_enrollment(item_id: int, db: AsyncSession = Depends(get_db)): return await require(Enrollment, item_id, db, 'Enrollment')
@app.put('/api/enrollments/{item_id}', response_model=EnrollmentResponse, tags=['Enrollments'])
async def update_enrollment(item_id: int, data: EnrollmentUpdate, db: AsyncSession = Depends(get_db)):
    item = await require(Enrollment, item_id, db, 'Enrollment')
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    await commit(db); await db.refresh(item); return item
@app.delete('/api/enrollments/{item_id}', status_code=204, tags=['Enrollments'])
async def delete_enrollment(item_id: int, db: AsyncSession = Depends(get_db)):
    await db.delete(await require(Enrollment, item_id, db, 'Enrollment')); await db.commit(); return Response(status_code=204)
