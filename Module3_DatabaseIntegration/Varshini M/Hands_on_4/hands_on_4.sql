explain SELECT s.first_name, s.last_name, c.course_name FROM enrollments e JOIN students s ON s.student_id = e.student_id JOIN courses c ON c.course_id = e.course_id WHERE s.enrollment_year = 2022;

+----+-------------+-------+------------+--------+-------------------------------+---------------+---------+-------------------------+------+----------+-------------+
| id | select_type | table | partitions | type   | possible_keys                 | key           | key_len | ref                     | rows | filtered | Extra       |
+----+-------------+-------+------------+--------+-------------------------------+---------------+---------+-------------------------+------+----------+-------------+
|  1 | SIMPLE      | s     | NULL       | ALL    | PRIMARY                       | NULL          | NULL    | NULL                    |   10 |    10.00 | Using where |
|  1 | SIMPLE      | e     | NULL       | ref    | kf_studenroll,fk_courseenroll | kf_studenroll | 5       | college_db.s.student_id |    1 |   100.00 | Using where |
|  1 | SIMPLE      | c     | NULL       | eq_ref | PRIMARY                       | PRIMARY       | 4       | college_db.e.course_id  |    1 |   100.00 | NULL        |
+----+-------------+-------+------------+--------+-------------------------------+---------------+---------+-------------------------+------+----------+-------------+
3 rows in set, 1 warning (0.05 sec)

it shows a full table scan as there are no indices used

the cost here is 10(number of rows examined)

create index idx_students_enrollment_year on students(enrollment_year);

create unique index idx_student_course on enrollments(student_id, course_id);

create index idx_course_code on courses(course_code);

+----+-------------+-------+------------+--------+--------------------------------------+------------------------------+---------+-------------------------+------+----------+--------------------------+
| id | select_type | table | partitions | type   | possible_keys                        | key                          | key_len | ref                     | rows | filtered | Extra                    |
+----+-------------+-------+------------+--------+--------------------------------------+------------------------------+---------+-------------------------+------+----------+--------------------------+
|  1 | SIMPLE      | s     | NULL       | ref    | PRIMARY,idx_students_enrollment_year | idx_students_enrollment_year | 5       | const                   |    5 |   100.00 | NULL                     |
|  1 | SIMPLE      | e     | NULL       | ref    | idx_student_course,fk_courseenroll   | idx_student_course           | 5       | college_db.s.student_id |    1 |   100.00 | Using where; Using index |
|  1 | SIMPLE      | c     | NULL       | eq_ref | PRIMARY                              | PRIMARY                      | 4       | college_db.e.course_id  |    1 |   100.00 | NULL                     |
+----+-------------+-------+------------+--------+--------------------------------------+------------------------------+---------+-------------------------+------+----------+--------------------------+
3 rows in set, 1 warning (0.00 sec)