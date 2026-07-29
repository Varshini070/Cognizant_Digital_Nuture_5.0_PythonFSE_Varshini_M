from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request

from app import db
from courses.models import Course, Department, Enrollment, Student

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


def bad_request(message):
    return jsonify({'status': 'error', 'message': message}), 400


def get_payload():
    return request.get_json(silent=True) or {}


def department_exists(department_id):
    return department_id is not None and db.session.get(Department, department_id) is not None


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json([course.to_dict() for course in Course.query.all()])


@courses_bp.route('/', methods=['POST'])
def create_course():
    payload = get_payload()
    required_fields = ['name', 'code', 'credits', 'department_id']
    missing = [field for field in required_fields if payload.get(field) is None or payload.get(field) == '']
    if missing:
        return bad_request(f'Missing required fields: {", ".join(missing)}')
    if not department_exists(payload['department_id']):
        return bad_request('Department not found')

    course = Course(
        name=payload['name'],
        code=payload['code'],
        credits=payload['credits'],
        department_id=payload['department_id'],
    )
    try:
        db.session.add(course)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return bad_request('Course code must be unique')
    return make_response_json(course.to_dict(), 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    return make_response_json(Course.query.get_or_404(course_id).to_dict())


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    payload = get_payload()
    for field in ('name', 'code', 'credits'):
        if field in payload:
            setattr(course, field, payload[field])
    if 'department_id' in payload:
        if not department_exists(payload['department_id']):
            return bad_request('Department not found')
        course.department_id = payload['department_id']
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return bad_request('Course code must be unique')
    return make_response_json(course.to_dict())


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return make_response_json({'message': 'Course deleted'})


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def list_course_students(course_id):
    Course.query.get_or_404(course_id)
    students = db.session.execute(
        db.select(Student).join(Enrollment).where(Enrollment.course_id == course_id)
    ).scalars().all()
    return make_response_json([student.to_dict() for student in students])
