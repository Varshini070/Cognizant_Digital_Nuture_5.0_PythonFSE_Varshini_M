# Hands-on 3: Django REST Framework API

This folder contains a DRF-based Course Management API with:

- Model serializers for Department, Course, Student, and Enrollment
- ViewSets for CRUD operations
- Router-based URL patterns under /api/
- A custom action at /api/courses/{id}/students/

Run:

- python manage.py runserver 127.0.0.1:8002
- Test endpoints such as /api/courses/ and /api/courses/1/students/
