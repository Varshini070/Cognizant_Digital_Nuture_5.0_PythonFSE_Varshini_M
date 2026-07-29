from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal, engine, get_db
from models import Base, Course, Department
from schemas import CourseCreate, CourseResponse, CourseUpdate


async def seed_data(session: AsyncSession):
    """Add small starter data so pagination can be tried immediately."""
    if (await session.execute(select(Department.id).limit(1))).scalar_one_or_none() is not None:
        return

    engineering = Department(name='Engineering', head_of_dept='Anita Rao', budget=500000)
    science = Department(name='Science', head_of_dept='Rahul Mehta', budget=350000)
    session.add_all([engineering, science])
    await session.flush()
    session.add_all([
        Course(name='Python Fundamentals', code='PY101', credits=4, department_id=engineering.id),
        Course(name='Web Development', code='WD201', credits=3, department_id=engineering.id),
        Course(name='Data Science', code='DS301', credits=4, department_id=science.id),
    ])
    await session.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_data(session)
    yield
    await engine.dispose()


app = FastAPI(title='Course Management API', version='1.0', lifespan=lifespan)


@app.get('/')
async def root():
    return {'message': 'API running'}


async def get_course_or_404(course_id: int, db: AsyncSession) -> Course:
    course = await db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    if await db.get(Department, course.department_id) is None:
        raise HTTPException(status_code=400, detail='Department not found')

    new_course = Course(**course.model_dump())
    db.add(new_course)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail='Course code must be unique')
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/', response_model=list[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    statement = select(Course).offset(skip).limit(limit)
    if department_id is not None:
        statement = statement.where(Course.department_id == department_id)
    result = await db.execute(statement)
    return result.scalars().all()


@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    return await get_course_or_404(course_id, db)


@app.put('/api/courses/{course_id}', response_model=CourseResponse)
async def update_course(course_id: int, course_update: CourseUpdate, db: AsyncSession = Depends(get_db)):
    course = await get_course_or_404(course_id, db)
    changes = course_update.model_dump(exclude_unset=True)
    if 'department_id' in changes and await db.get(Department, changes['department_id']) is None:
        raise HTTPException(status_code=400, detail='Department not found')
    for field, value in changes.items():
        setattr(course, field, value)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail='Course code must be unique')
    await db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await get_course_or_404(course_id, db)
    await db.delete(course)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
