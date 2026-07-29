# Hands-on 5: Flask ORM Course Management API

This Flask API uses Flask-SQLAlchemy and Flask-Migrate with SQLite. It stores departments, courses, students, and enrollments in a real database.

## Setup and migrations

```powershell
cd handson_05
python -m pip install -r requirements.txt
flask --app app db init
flask --app app db migrate -m "initial schema"
flask --app app db upgrade
python app.py
```

The database file is created in Flask's `instance` directory.

## Seed data in the Flask shell

```powershell
flask --app app shell
```

```python
from app import db
from courses.models import Department, Course

engineering = Department(name='Engineering', head_of_dept='Anita Rao', budget=500000)
science = Department(name='Science', head_of_dept='Rahul Mehta', budget=350000)
db.session.add_all([engineering, science])
db.session.commit()

db.session.add_all([
    Course(name='Python Fundamentals', code='PY101', credits=4, department_id=engineering.id),
    Course(name='Web Development', code='WD201', credits=3, department_id=engineering.id),
    Course(name='Data Science', code='DS301', credits=4, department_id=science.id),
])
db.session.commit()
```

## API endpoints

- `GET`, `POST` `/api/courses/`
- `GET`, `PUT`, `DELETE` `/api/courses/<id>/`
- `GET` `/api/courses/<id>/students/`

POST a course with `name`, `code`, `credits`, and `department_id`.
