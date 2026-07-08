Tables after insertion
mysql> select * from courses;
+-----------+------------------------------+-------------+---------+---------------+-----------+
| course_id | course_name                  | course_code | credits | department_id | max_seats |
+-----------+------------------------------+-------------+---------+---------------+-----------+
|         1 | Data Structures & Algorithms | CS101       |       4 |             1 |        60 |
|         2 | Database Management Systems  | CS102       |       3 |             1 |        60 |
|         3 | Object Oriented Programming  | CS103       |       4 |             1 |        60 |
|         4 | Circuit Theory               | EC101       |       3 |             2 |        60 |
|         5 | Thermodynamics               | ME101       |       3 |             3 |        60 |
+-----------+------------------------------+-------------+---------+---------------+-----------+
5 rows in set (0.06 sec)

mysql> select * from departments;
+---------------+------------------+-------------------+-----------+
| department_id | dept_name        | head_of_dept      | budget    |
+---------------+------------------+-------------------+-----------+
|             1 | Computer Science | Dr. Ramesh Kumar  | 850000.00 |
|             2 | Electronics      | Dr. Priya Nair    | 620000.00 |
|             3 | Mechanical       | Dr. Suresh Iyer   | 540000.00 |
|             4 | Civil            | Dr. Ananya Sharma | 430000.00 |
+---------------+------------------+-------------------+-----------+
4 rows in set (0.01 sec)

mysql> select * from enrollments;
+---------------+------------+-----------+-----------------+-------+
| enrollment_id | student_id | course_id | enrollment_date | grade |
+---------------+------------+-----------+-----------------+-------+
|             1 |          1 |         1 | 2022-07-01      | A     |
|             2 |          1 |         2 | 2022-07-01      | B     |
|             3 |          2 |         1 | 2022-07-01      | B     |
|             4 |          2 |         3 | 2022-07-01      | A     |
|             5 |          3 |         4 | 2021-07-01      | A     |
|             6 |          4 |         5 | 2023-07-01      | NULL  |
|             7 |          5 |         1 | 2022-07-01      | C     |
|             8 |          5 |         2 | 2022-07-01      | A     |
|             9 |          6 |         4 | 2021-07-01      | B     |
|            10 |          7 |         5 | 2023-07-01      | NULL  |
|            11 |          8 |         1 | 2022-07-01      | A     |
|            12 |          8 |         3 | 2022-07-01      | B     |
+---------------+------------+-----------+-----------------+-------+
12 rows in set (0.01 sec)

mysql> select * from professors;
+--------------+--------------------+----------------------+---------------+----------+
| professor_id | prof_name          | email                | department_id | salary   |
+--------------+--------------------+----------------------+---------------+----------+
|            1 | Dr. Anand Krishnan | anand.k@college.edu  |             1 | 95000.00 |
|            2 | Dr. Meena Pillai   | meena.p@college.edu  |             1 | 88000.00 |
|            3 | Dr. Sunil Rajan    | sunil.r@college.edu  |             2 | 82000.00 |
|            4 | Dr. Latha Gopal    | latha.g@college.edu  |             3 | 79000.00 |
|            5 | Dr. Kartik Bose    | kartik.b@college.edu |             4 | 76000.00 |
+--------------+--------------------+----------------------+---------------+----------+
5 rows in set (0.00 sec)

mysql> select * from students;
+------------+------------+-----------+--------------------------+---------------+---------------+-----------------+
| student_id | first_name | last_name | email                    | date_of_birth | department_id | enrollment_year |
+------------+------------+-----------+--------------------------+---------------+---------------+-----------------+
|          1 | Arjun      | Mehta     | arjun.mehta@college.edu  | 2003-04-12    |             1 |            2022 |
|          2 | Priya      | Suresh    | priya.suresh@college.edu | 2003-07-25    |             1 |            2022 |
|          3 | Rohan      | Verma     | rohan.verma@college.edu  | 2002-11-08    |             2 |            2021 |
|          4 | Sneha      | Patel     | sneha.patel@college.edu  | 2004-01-30    |             3 |            2023 |
|          5 | Vikram     | Das       | vikram.das@college.edu   | 2003-09-14    |             1 |            2022 |
|          6 | Kavya      | Menon     | kavya.menon@college.edu  | 2002-05-17    |             2 |            2021 |
|          7 | Aditya     | Singh     | aditya.singh@college.edu | 2004-03-22    |             4 |            2023 |
|          8 | Deepika    | Rao       | deepika.rao@college.edu  | 2003-08-09    |             1 |            2022 |
+------------+------------+-----------+--------------------------+---------------+---------------+-----------------+
8 rows in set (0.00 sec)

mysql> insert into students values(9,"Shobana","Reddy","shobana.reddy@college.edu",'2002-10-02',2,2021);
Query OK, 1 row affected (0.06 sec)

mysql> insert into students values(10,"Preethi","Kumar","preethi.kumar@college.edu",'2003-03-12',4,2022);
Query OK, 1 row affected (0.01 sec)

mysql> select * from students;
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
| student_id | first_name | last_name | email                     | date_of_birth | department_id | enrollment_year |
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
|          1 | Arjun      | Mehta     | arjun.mehta@college.edu   | 2003-04-12    |             1 |            2022 |
|          2 | Priya      | Suresh    | priya.suresh@college.edu  | 2003-07-25    |             1 |            2022 |
|          3 | Rohan      | Verma     | rohan.verma@college.edu   | 2002-11-08    |             2 |            2021 |
|          4 | Sneha      | Patel     | sneha.patel@college.edu   | 2004-01-30    |             3 |            2023 |
|          5 | Vikram     | Das       | vikram.das@college.edu    | 2003-09-14    |             1 |            2022 |
|          6 | Kavya      | Menon     | kavya.menon@college.edu   | 2002-05-17    |             2 |            2021 |
|          7 | Aditya     | Singh     | aditya.singh@college.edu  | 2004-03-22    |             4 |            2023 |
|          8 | Deepika    | Rao       | deepika.rao@college.edu   | 2003-08-09    |             1 |            2022 |
|          9 | Shobana    | Reddy     | shobana.reddy@college.edu | 2002-10-02    |             2 |            2021 |
|         10 | Preethi    | Kumar     | preethi.kumar@college.edu | 2003-03-12    |             4 |            2022 |
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
10 rows in set (0.00 sec)

mysql> update enrollments set grade = 'B' where student_id = 5 and course_id = 1;
Query OK, 1 row affected (0.04 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from enrollments where student_id = 5 and course_id = 1;
+---------------+------------+-----------+-----------------+-------+
| enrollment_id | student_id | course_id | enrollment_date | grade |
+---------------+------------+-----------+-----------------+-------+
|             7 |          5 |         1 | 2022-07-01      | B     |
+---------------+------------+-----------+-----------------+-------+
1 row in set (0.00 sec)

mysql> SELECT * FROM enrollments WHERE grade IS NULL;
+---------------+------------+-----------+-----------------+-------+
| enrollment_id | student_id | course_id | enrollment_date | grade |
+---------------+------------+-----------+-----------------+-------+
|             6 |          4 |         5 | 2023-07-01      | NULL  |
|            10 |          7 |         5 | 2023-07-01      | NULL  |
+---------------+------------+-----------+-----------------+-------+
2 rows in set (0.00 sec)

mysql> delete from enrollments where grade is null;
Query OK, 2 rows affected (0.01 sec)

mysql> SELECT * FROM enrollments WHERE grade IS NULL;
Empty set (0.00 sec)

mysql> select count(*) from students;
+----------+
| count(*) |
+----------+
|       10 |
+----------+
1 row in set (0.01 sec)

mysql> select count(*) from enrollments;
+----------+
| count(*) |
+----------+
|       10 |
+----------+
1 row in set (0.00 sec)

mysql> select count(*) from departments;
+----------+
| count(*) |
+----------+
|        4 |
+----------+
1 row in set (0.02 sec)

mysql> select count(*) from professors;
+----------+
| count(*) |
+----------+
|        5 |
+----------+
1 row in set (0.00 sec)

mysql> select count(*) from courses;
+----------+
| count(*) |
+----------+
|        5 |
+----------+
1 row in set (0.00 sec)

mysql> select * from students where enrollment_year=2022 order by last_name;
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
| student_id | first_name | last_name | email                     | date_of_birth | department_id | enrollment_year |
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
|          5 | Vikram     | Das       | vikram.das@college.edu    | 2003-09-14    |             1 |            2022 |
|         10 | Preethi    | Kumar     | preethi.kumar@college.edu | 2003-03-12    |             4 |            2022 |
|          1 | Arjun      | Mehta     | arjun.mehta@college.edu   | 2003-04-12    |             1 |            2022 |
|          8 | Deepika    | Rao       | deepika.rao@college.edu   | 2003-08-09    |             1 |            2022 |
|          2 | Priya      | Suresh    | priya.suresh@college.edu  | 2003-07-25    |             1 |            2022 |
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
5 rows in set (0.00 sec)

mysql> select * from courses where credits>3 order by credits desc;
+-----------+------------------------------+-------------+---------+---------------+-----------+
| course_id | course_name                  | course_code | credits | department_id | max_seats |
+-----------+------------------------------+-------------+---------+---------------+-----------+
|         1 | Data Structures & Algorithms | CS101       |       4 |             1 |        60 |
|         3 | Object Oriented Programming  | CS103       |       4 |             1 |        60 |
+-----------+------------------------------+-------------+---------+---------------+-----------+
2 rows in set (0.00 sec)

mysql> select * from professors where salary between 80000 and 95000;
+--------------+--------------------+---------------------+---------------+----------+
| professor_id | prof_name          | email               | department_id | salary   |
+--------------+--------------------+---------------------+---------------+----------+
|            1 | Dr. Anand Krishnan | anand.k@college.edu |             1 | 95000.00 |
|            2 | Dr. Meena Pillai   | meena.p@college.edu |             1 | 88000.00 |
|            3 | Dr. Sunil Rajan    | sunil.r@college.edu |             2 | 82000.00 |
+--------------+--------------------+---------------------+---------------+----------+
3 rows in set (0.00 sec)

mysql> select * from students where email like '%@college.edu';
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
| student_id | first_name | last_name | email                     | date_of_birth | department_id | enrollment_year |
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
|          1 | Arjun      | Mehta     | arjun.mehta@college.edu   | 2003-04-12    |             1 |            2022 |
|          2 | Priya      | Suresh    | priya.suresh@college.edu  | 2003-07-25    |             1 |            2022 |
|          3 | Rohan      | Verma     | rohan.verma@college.edu   | 2002-11-08    |             2 |            2021 |
|          4 | Sneha      | Patel     | sneha.patel@college.edu   | 2004-01-30    |             3 |            2023 |
|          5 | Vikram     | Das       | vikram.das@college.edu    | 2003-09-14    |             1 |            2022 |
|          6 | Kavya      | Menon     | kavya.menon@college.edu   | 2002-05-17    |             2 |            2021 |
|          7 | Aditya     | Singh     | aditya.singh@college.edu  | 2004-03-22    |             4 |            2023 |
|          8 | Deepika    | Rao       | deepika.rao@college.edu   | 2003-08-09    |             1 |            2022 |
|          9 | Shobana    | Reddy     | shobana.reddy@college.edu | 2002-10-02    |             2 |            2021 |
|         10 | Preethi    | Kumar     | preethi.kumar@college.edu | 2003-03-12    |             4 |            2022 |
+------------+------------+-----------+---------------------------+---------------+---------------+-----------------+
10 rows in set (0.00 sec)

mysql> select enrollment_year, count(student_id) as student_count from students group by enrollment_year;
+-----------------+---------------+
| enrollment_year | student_count |
+-----------------+---------------+
|            2022 |             5 |
|            2021 |             3 |
|            2023 |             2 |
+-----------------+---------------+
3 rows in set (0.00 sec)

mysql> select concat(s.first_name,' ',s.last_name) as full_name,d.dept_name from students s inner join departments d on s.department_id = d.department_id;
+---------------+------------------+
| full_name     | dept_name        |
+---------------+------------------+
| Arjun Mehta   | Computer Science |
| Priya Suresh  | Computer Science |
| Vikram Das    | Computer Science |
| Deepika Rao   | Computer Science |
| Rohan Verma   | Electronics      |
| Kavya Menon   | Electronics      |
| Shobana Reddy | Electronics      |
| Sneha Patel   | Mechanical       |
| Aditya Singh  | Civil            |
| Preethi Kumar | Civil            |
+---------------+------------------+
10 rows in set (0.00 sec)

mysql> select e.enrollment_id, e.enrollment_date, e.grade, concat(s.first_name,' ',s.last_name) as student_name, c.course_name from enrollments e inner join students s on e.student_id = s.student_id inner join courses c on e.course_id = c.course_id;
+---------------+-----------------+-------+--------------+------------------------------+
| enrollment_id | enrollment_date | grade | student_name | course_name                  |
+---------------+-----------------+-------+--------------+------------------------------+
|             1 | 2022-07-01      | A     | Arjun Mehta  | Data Structures & Algorithms |
|             2 | 2022-07-01      | B     | Arjun Mehta  | Database Management Systems  |
|             3 | 2022-07-01      | B     | Priya Suresh | Data Structures & Algorithms |
|             4 | 2022-07-01      | A     | Priya Suresh | Object Oriented Programming  |
|             5 | 2021-07-01      | A     | Rohan Verma  | Circuit Theory               |
|             7 | 2022-07-01      | B     | Vikram Das   | Data Structures & Algorithms |
|             8 | 2022-07-01      | A     | Vikram Das   | Database Management Systems  |
|             9 | 2021-07-01      | B     | Kavya Menon  | Circuit Theory               |
|            11 | 2022-07-01      | A     | Deepika Rao  | Data Structures & Algorithms |
|            12 | 2022-07-01      | B     | Deepika Rao  | Object Oriented Programming  |
+---------------+-----------------+-------+--------------+------------------------------+
10 rows in set (0.00 sec)

mysql> select s.student_id, concat(s.first_name,' ',s.last_name) as student_name from students s left join enrollments e on s.student_id =e.student_id where e.course_id is null;
+------------+---------------+
| student_id | student_name  |
+------------+---------------+
|          4 | Sneha Patel   |
|          7 | Aditya Singh  |
|          9 | Shobana Reddy |
|         10 | Preethi Kumar |
+------------+---------------+
4 rows in set (0.01 sec)

mysql> select c.course_name, count(e.student_id) from courses c left join enrollments e on c.course_id = e.course_id group by c.course_name;
+------------------------------+---------------------+
| course_name                  | count(e.student_id) |
+------------------------------+---------------------+
| Data Structures & Algorithms |                   4 |
| Database Management Systems  |                   2 |
| Object Oriented Programming  |                   2 |
| Circuit Theory               |                   2 |
| Thermodynamics               |                   0 |
+------------------------------+---------------------+
5 rows in set (0.00 sec)

mysql> select d.dept_name,p.prof_name,p.salary from departments d left join professors p on d.department_id=p.department_id;
+------------------+--------------------+----------+
| dept_name        | prof_name          | salary   |
+------------------+--------------------+----------+
| Computer Science | Dr. Anand Krishnan | 95000.00 |
| Computer Science | Dr. Meena Pillai   | 88000.00 |
| Electronics      | Dr. Sunil Rajan    | 82000.00 |
| Mechanical       | Dr. Latha Gopal    | 79000.00 |
| Civil            | Dr. Kartik Bose    | 76000.00 |
+------------------+--------------------+----------+
5 rows in set (0.00 sec)

mysql> select c.course_name, count(e.student_id) from courses c left join enrollments e on c.course_id = e.course_id group by c.course_name;
+------------------------------+---------------------+
| course_name                  | count(e.student_id) |
+------------------------------+---------------------+
| Data Structures & Algorithms |                   4 |
| Database Management Systems  |                   2 |
| Object Oriented Programming  |                   2 |
| Circuit Theory               |                   2 |
| Thermodynamics               |                   0 |
+------------------------------+---------------------+
5 rows in set (0.00 sec)

mysql> select d.dept_name, round(avg(p.salary),2) as average_salary from departments d left join professors p on d.department_id = p.department_id group by d.dept_name;
+------------------+----------------+
| dept_name        | average_salary |
+------------------+----------------+
| Computer Science |       91500.00 |
| Electronics      |       82000.00 |
| Mechanical       |       79000.00 |
| Civil            |       76000.00 |
+------------------+----------------+
4 rows in set (0.01 sec)

mysql> select e.grade, count(e.student_id) from enrollments as e where e.course_id = (select course_id from courses where course_code = 'CS101') group by e.grade;
+-------+---------------------+
| grade | count(e.student_id) |
+-------+---------------------+
| A     |                   2 |
| B     |                   2 |
+-------+---------------------+
2 rows in set (0.01 sec)

mysql> select d.dept_name,count(e.student_id) from departments d inner join courses c on d.department_id = c.department_id inner join enrollments e on e.course_id = c.course_id group by d.dept_name having count(e.student_id)>2;
+------------------+---------------------+
| dept_name        | count(e.student_id) |
+------------------+---------------------+
| Computer Science |                   8 |
+------------------+---------------------+
1 row in set (0.00 sec)

