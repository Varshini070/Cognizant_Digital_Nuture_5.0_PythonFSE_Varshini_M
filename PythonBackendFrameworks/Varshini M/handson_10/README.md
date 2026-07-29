# Hands-on 10: Course Management Microservices

| Service | Responsibility | Endpoints it owns | Database it owns |
|---|---|---|---|
| Course Service | Departments and courses | `/api/courses/*` | `course_service/courses.db` |
| Student Service | Students and enrollment records | `/api/students/*` | `student_service/students.db` |
| Auth Service | Registration, login, token validation | `/api/auth/*` | Its own users database (future service) |
| Notification Service | Enrollment email confirmations | `/api/notifications/*` | Its own delivery database/queue (future service) |

## Run

In three terminals, install dependencies in the `handson_10` folder, then run:

```powershell
cd course_service; python app.py       # port 5001
cd student_service; python app.py      # port 5002
cd gateway; python app.py              # port 5000
```

Try `POST http://localhost:5000/api/students/1/enroll` with `{"course_id": 1}`. The gateway forwards it to Student Service, which verifies the course through Course Service.

Synchronous HTTP is simple, immediate, and suited to request/response operations, but it couples availability and latency across services. Message queues such as RabbitMQ or Kafka are preferable for durable, high-volume, retryable, or eventually consistent work (for example notifications and audit events); they trade immediate results for operational complexity and eventual consistency.
