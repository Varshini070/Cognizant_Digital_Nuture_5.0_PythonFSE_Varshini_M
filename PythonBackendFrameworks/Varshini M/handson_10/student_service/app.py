import os
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

COURSE_SERVICE_URL = os.getenv('COURSE_SERVICE_URL', 'http://localhost:5001')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True); name = db.Column(db.String(200), nullable=False); email = db.Column(db.String(120), unique=True, nullable=False)
    def to_dict(self): return {'id': self.id, 'name': self.name, 'email': self.email}
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True); student_id = db.Column(db.Integer, nullable=False); course_id = db.Column(db.Integer, nullable=False)
with app.app_context():
    db.create_all()
    if not Student.query.first(): db.session.add(Student(name='Varshini', email='varshini@example.com')); db.session.commit()
@app.get('/api/students/')
def students(): return jsonify([student.to_dict() for student in Student.query.all()])
@app.post('/api/students/')
def create_student():
    data = request.get_json() or {}; item = Student(name=data.get('name', ''), email=data.get('email', ''))
    if not item.name or not item.email: return jsonify({'error': 'name and email are required'}), 400
    db.session.add(item); db.session.commit(); return jsonify(item.to_dict()), 201
@app.post('/api/students/<int:student_id>/enroll')
def enroll(student_id):
    db.get_or_404(Student, student_id); course_id = (request.get_json() or {}).get('course_id')
    if not course_id: return jsonify({'error': 'course_id is required'}), 400
    try: response = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{course_id}/', timeout=3)
    except requests.ConnectionError: return jsonify({'error': 'Course Service is unavailable; enrollment cannot be verified'}), 503
    if response.status_code == 404: return jsonify({'error': 'Course not found'}), 404
    if not response.ok: return jsonify({'error': 'Course Service returned an error'}), 503
    item = Enrollment(student_id=student_id, course_id=course_id); db.session.add(item); db.session.commit()
    return jsonify({'id': item.id, 'student_id': student_id, 'course_id': course_id}), 201
if __name__ == '__main__': app.run(port=5002, debug=True)
