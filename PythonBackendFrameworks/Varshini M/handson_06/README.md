# Hands-on 6: FastAPI Course Management API

FastAPI rebuild of the Course API with Pydantic validation and async SQLAlchemy.

## Run

```powershell
cd handson_06
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for Swagger UI and the generated OpenAPI schemas.

The application creates `courses.db` and seeds two departments with three courses when first started.

## Endpoints

- `GET /` — service status
- `POST /api/courses/` — create a course
- `GET /api/courses/?skip=0&limit=2&department_id=1` — paginated/filterable list
- `GET /api/courses/{course_id}` — retrieve one course
- `PUT /api/courses/{course_id}` — update selected fields
- `DELETE /api/courses/{course_id}` — delete a course

Example create body:

```json
{
  "name": "Database Systems",
  "code": "DB401",
  "credits": 4,
  "department_id": 1
}
```
