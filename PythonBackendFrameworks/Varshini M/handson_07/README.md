# Hands-on 7

Run `uvicorn main:app --reload`, then open `/docs`. Endpoints are grouped as Courses, Students, and Enrollments. Enrollment creation returns `201` and schedules its confirmation-print task after the response is sent.
