import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="college_db"
)

cursor = conn.cursor()

start = time.time()

query_count = 1

cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()

for enrollment in enrollments:
    cursor.execute(
        "SELECT first_name,last_name FROM students WHERE student_id=%s",
        (enrollment[1],)
    )
    cursor.fetchone()
    query_count += 1

end = time.time()

print("N+1: Queries Executed-", query_count)
print("Time:", end-start)

start = time.time()

cursor.execute("""
SELECT
s.first_name,
s.last_name,
c.course_name
FROM enrollments e
JOIN students s
ON e.student_id=s.student_id
JOIN courses c
ON e.course_id=c.course_id
""")

rows = cursor.fetchall()

end = time.time()

print("Join: Queries Executed- 1")
print("Time:", end-start)

#in a real application with 10000 enrollments, the n+1 version will take 10001 queries while the join will only take 1 query which gives better performance