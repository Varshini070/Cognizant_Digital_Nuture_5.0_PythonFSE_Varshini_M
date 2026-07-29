from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from security import get_password_hash, verify_password

SECRET_KEY = 'replace-this-development-secret-before-production'
ALGORITHM = 'HS256'; ACCESS_TOKEN_MINUTES = 30
engine = create_async_engine('sqlite+aiosqlite:///./courses.db'); Sessions = async_sessionmaker(engine, expire_on_commit=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/')
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True); email: Mapped[str] = mapped_column(String(120), unique=True); hashed_password: Mapped[str] = mapped_column(String(255)); is_active: Mapped[bool] = mapped_column(Boolean, default=True)
class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(primary_key=True); name: Mapped[str] = mapped_column(String(200)); code: Mapped[str] = mapped_column(String(20), unique=True); credits: Mapped[int] = mapped_column(Integer); department_id: Mapped[int] = mapped_column(Integer)
class RegisterRequest(BaseModel): email: EmailStr; password: str = Field(min_length=8)
class LoginRequest(BaseModel): email: EmailStr; password: str
class UserResponse(BaseModel): model_config = ConfigDict(from_attributes=True); id: int; email: EmailStr; is_active: bool
class CourseCreate(BaseModel): name: str; code: str; credits: int = Field(gt=0); department_id: int = Field(gt=0)
class CourseResponse(BaseModel): model_config = ConfigDict(from_attributes=True); id: int; name: str; code: str; credits: int; department_id: int
async def get_db():
    async with Sessions() as db: yield db
def make_token(user: User): return jwt.encode({'sub': str(user.id), 'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try: user_id = int(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('sub'))
    except (JWTError, TypeError, ValueError): raise HTTPException(401, 'Invalid or expired token', headers={'WWW-Authenticate': 'Bearer'})
    user = await db.get(User, user_id)
    if not user or not user.is_active: raise HTTPException(401, 'Invalid or expired token', headers={'WWW-Authenticate': 'Bearer'})
    return user
@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    yield; await engine.dispose()
app = FastAPI(title='Secure Course Management API', version='1.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3000'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
# OAuth2 Authorization Code redirects a user to an identity provider and exchanges an authorization code server-side.
# This demo instead verifies credentials directly and issues a JWT; it is simpler but not a replacement for OAuth2 SSO.
@app.post('/api/v1/auth/register/', response_model=UserResponse, status_code=201, tags=['Auth'])
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none(): raise HTTPException(409, 'Email already registered')
    user = User(email=data.email, hashed_password=get_password_hash(data.password)); db.add(user)
    try: await db.commit()
    except IntegrityError: await db.rollback(); raise HTTPException(409, 'Email already registered')
    await db.refresh(user); return user
@app.post('/api/v1/auth/login/', tags=['Auth'])
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password): raise HTTPException(401, 'Incorrect email or password', headers={'WWW-Authenticate': 'Bearer'})
    return {'access_token': make_token(user), 'token_type': 'bearer'}
@app.get('/api/v1/courses/', response_model=list[CourseResponse], tags=['Courses'])
async def list_courses(db: AsyncSession = Depends(get_db)): return (await db.execute(select(Course))).scalars().all()
@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=201, tags=['Courses'])
async def create_course(data: CourseCreate, response: Response, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    item = Course(**data.model_dump()); db.add(item); await db.commit(); await db.refresh(item); response.headers['Location'] = f'/api/v1/courses/{item.id}/'; return item
@app.delete('/api/v1/courses/{course_id}/', status_code=204, tags=['Courses'])
async def delete_course(course_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    item = await db.get(Course, course_id)
    if not item: raise HTTPException(404, 'Course not found')
    await db.delete(item); await db.commit(); return Response(status_code=204)
