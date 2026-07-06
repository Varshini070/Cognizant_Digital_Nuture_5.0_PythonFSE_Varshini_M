create database college_db;

create table departments (department_id int primary key auto_increment, dept_name varchar(100) not null, hod_name varchar(100) comment 'Head of Department', budget decimal(12,2));

create table students (student_id int primary key auto_increment, first_name varchar(50) not null, last_name varchar(50) not null, email varchar(100) unique not null, date_of_birth date, department_id int, enrollment_year int, constraint fkey_deptstud foreign key(department_id) references departments(department_id));

create table courses (course_id int primary key auto_increment, course_name varchar(150) not null, course_code varchar(20) unique, credits int, department_id int, constraint fkey_deptcourse foreign key(department_id) references departments(department_id));

create table enrollments (enrollment_id int primary key auto_increment, student_id int, course_id int, enrollment_date date, grade char(2) null, constraint kf_studenroll foreign key (student_id) references students(student_id), constraint fk_courseenroll foreign key (course_id) references courses(course_id));
/*1NF: The attributes are indivisible and unique, therefore it satisfies first normal form.
2NF: As there is no composite key for primary key and all attributes are dependent on the primary key it satisfies second normal form.
3NF: The table is in 2NF, and there are no transitive dependencies among non-key attributes. The references are also mentioned only using the foreign key hence it satisfies third normal form.*/

create table professors (professor_id int primary key auto_increment, prof_name varchar(100) not null, email varchar(100) unique, department_id int, salary decimal(10,2), constraint fk_profdept foreign key (department_id) references departments(department_id));

alter table students add column phone_number varchar(15);

alter table courses add column max_seats int default 60;

alter table enrollments add constraint chk_enroll_grade check(grade in ('A','B','C','D','F') or grade is null);

alter table departments rename column hod_name to head_of_dept;

alter table students drop column phone_number;
