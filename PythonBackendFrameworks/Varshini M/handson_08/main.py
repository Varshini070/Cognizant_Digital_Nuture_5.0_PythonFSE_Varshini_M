"""Hands-on 8: REST naming, API versioning, pagination, and uniform errors."""
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import Integer, String, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict, Field

engine = create_async_engine('sqlite+aiosqlite:///./courses.db')
Sessions = async_sessionmaker(engine, expire_on_commit=False)
class Base(DeclarativeBase): pass
class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(200)); code: Mapped[str] = mapped_column(String(20), unique=True); credits: Mapped[int] = mapped_column(Integer); department_id: Mapped[int] = mapped_column(Integer)
class CourseCreate(BaseModel): name: str = Field(min_length=1); code: str = Field(min_length=1); credits: int = Field(gt=0); department_id: int = Field(gt=0)
class CourseUpdate(BaseModel): name: str | None = None; code: str | None = None; credits: int | None = Field(default=None, gt=0); department_id: int | None = Field(default=None, gt=0)
class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; name: str; code: str; credits: int; department_id: int

# URL versioning is visible and simple. Header versioning (Accept: application/vnd.api+json;version=1)
# keeps URLs stable but is less discoverable in browsers and documentation tools.
async def get_db():
    async with Sessions() as db: yield db
def error(code, message, field=None, status_code=400): return JSONResponse(status_code=status_code, content={'error': {'code': code, 'message': message, 'field': field}})
@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    async with Sessions() as db:
        if not (await db.execute(select(Course.id).limit(1))).scalar_one_or_none():
            db.add_all([Course(name='Python Fundamentals', code='PY101', credits=4, department_id=1), Course(name='Web Development', code='WD201', credits=3, department_id=1), Course(name='Data Science', code='DS301', credits=4, department_id=2)]); await db.commit()
    yield; await engine.dispose()
app = FastAPI(title='Course Management API', version='1.2', lifespan=lifespan)
@app.exception_handler(HTTPException)
async def http_error(_: Request, exc: HTTPException):
    code = 'NOT_FOUND' if exc.status_code == 404 else 'UNAUTHORISED' if exc.status_code == 401 else 'BAD_REQUEST'
    return error(code, str(exc.detail), status_code=exc.status_code)
@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    issue = exc.errors()[0]; return error('VALIDATION_ERROR', issue['msg'], '.'.join(map(str, issue['loc'])), 422)
async def find(course_id, db):
    item = await db.get(Course, course_id)
    if not item: raise HTTPException(404, f'Course with id {course_id} does not exist')
    return item
@app.get('/api/v1/courses/', tags=['Courses'])
async def list_courses(request: Request, page: int = 1, page_size: int = 10, search: str | None = None, db: AsyncSession = Depends(get_db)):
    if page < 1 or page_size < 1: raise HTTPException(400, 'page and page_size must be positive')
    stmt = select(Course)
    if search:
        term = f'%{search.lower()}%'; stmt = stmt.where(func.lower(Course.name).like(term) | func.lower(Course.code).like(term))
    count = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    results = (await db.execute(stmt.offset((page - 1) * page_size).limit(page_size))).scalars().all()
    def url(target): return str(request.url.include_query_params(page=target))
    return {'count': count, 'next': url(page + 1) if page * page_size < count else None, 'previous': url(page - 1) if page > 1 else None, 'results': [CourseResponse.model_validate(x).model_dump() for x in results]}
@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=201, tags=['Courses'])
async def create_course(data: CourseCreate, response: Response, db: AsyncSession = Depends(get_db)):
    item = Course(**data.model_dump()); db.add(item)
    try: await db.commit()
    except IntegrityError: await db.rollback(); raise HTTPException(400, 'Course code already exists')
    await db.refresh(item); response.headers['Location'] = f'/api/v1/courses/{item.id}/'; return item
@app.get('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)): return await find(course_id, db)
@app.put('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def replace_course(course_id: int, data: CourseCreate, db: AsyncSession = Depends(get_db)):
    item = await find(course_id, db)
    for key, value in data.model_dump().items(): setattr(item, key, value)
    await db.commit(); await db.refresh(item); return item
@app.patch('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def patch_course(course_id: int, data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    item = await find(course_id, db)
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    await db.commit(); await db.refresh(item); return item
@app.delete('/api/v1/courses/{course_id}/', status_code=204, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    await db.delete(await find(course_id, db)); await db.commit(); return Response(status_code=204)
