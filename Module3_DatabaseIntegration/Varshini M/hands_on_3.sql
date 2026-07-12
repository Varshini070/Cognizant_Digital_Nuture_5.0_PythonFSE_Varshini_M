select s.student_id, concat(s.first_name,' ',s.last_name) as student_name, COUNT(e.course_id) as total_courses from students s join enrollments e on s.student_id = e.student_id group by s.student_id having count(e.course_id) > (select avg(course_count) from(select count(*) as course_count from enrollments group by student_id) as avg_count);

select c.course_id, c.course_name from courses c where not exists (select * from enrollments e where e.course_id = c.course_id and e.grade <= 'A');

select p.professor_id, p.prof_name, p.department_id from professors p where p.salary = (select max(salary) from professors where department_id = p.department_id);

select * from (select department_id, avg(salary) as avg_salary from professors group by department_id) as avg_salary_table where avg_salary>85000;

create view vw_student_enrollment_summary as select s.student_id, concat(s.first_name,' ',s.last_name) as full_name, d.dept_name, count(e.course_id) as total_courses, avg(case when e.grade='A' then 4 when e.grade='B' then 3 when e.grade='C' then 2 when e.grade='D' then 1 when e.grade='F' then 0 end) as gpa from students s join departments d on s.department_id=d.department_id left join enrollments e on s.student_id=e.student_id group by s.student_id;

create view vw_course_stats as select c.course_name, c.course_code, count(e.enrollment_id) as total_enrollments, avg(case when e.grade='A' then 4 when e.grade='B' then 3 when e.grade='C' then 2 when e.grade='D' then 1 when e.grade='F' then 0 end) as avg_gpa from courses c left join enrollments e on c.course_id=e.course_id group by c.course_code;

select * from vw_student_enrollment_summary where gpa > 3.0;

create procedure sp_enroll_student(in p_student_id int, in p_course_id int, in p_enrollment_date date)
begin
if exists(select * from enrollments where student_id=p_student_id and course_id=p_course_id) then signal sqlstate '45000' set message_text='Student already enrolled';
else insert into enrollments(student_id,course_id,enrollment_date) values(p_student_id,p_course_id,p_enrollment_date);
end if;
end//

create table department_transfer_log (log_id int auto_increment primary key, student_id INT, old_department INT, new_department INT, transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)//

CREATE PROCEDURE sp_transfer_student(IN p_student INT, IN p_new_dept INT)
BEGIN
DECLARE old_dept INT;
START TRANSACTION;
SELECT department_id INTO old_dept FROM students WHERE student_id=p_student;
UPDATE students SET department_id=p_new_dept WHERE student_id=p_student;
INSERT INTO department_transfer_log (student_id,old_department,new_department) VALUES (p_student,old_dept,p_new_dept);
COMMIT;
END//

