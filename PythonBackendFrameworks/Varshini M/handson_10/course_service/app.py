from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    def to_dict(self): return {'id': self.id, 'name': self.name, 'code': self.code, 'credits': self.credits}

with app.app_context():
    db.create_all()
    if not Course.query.first():
        db.session.add_all([Course(name='Python Fundamentals', code='PY101', credits=4), Course(name='Web Development', code='WD201', credits=3)])
        db.session.commit()

@app.get('/api/courses/')
def courses(): return jsonify([course.to_dict() for course in Course.query.all()])
@app.post('/api/courses/')
def create_course():
    data = request.get_json() or {}
    if not all(data.get(k) for k in ('name', 'code', 'credits')): return jsonify({'error': 'name, code, and credits are required'}), 400
    course = Course(name=data['name'], code=data['code'], credits=data['credits']); db.session.add(course); db.session.commit()
    return jsonify(course.to_dict()), 201
@app.get('/api/courses/<int:course_id>/')
def course(course_id):
    item = db.get_or_404(Course, course_id); return jsonify(item.to_dict())

if __name__ == '__main__': app.run(port=5001, debug=True)
