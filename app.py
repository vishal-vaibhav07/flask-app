from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'students.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    reg_no = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        reg_no = request.form['reg_no']
        city = request.form['city']
        new_student = Student(name=name, department=department, reg_no=reg_no, city=city)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students'))
    
    # Handle search functionality
    search_query = request.args.get('search', '')
    if search_query:
        all_students = Student.query.filter(Student.name.ilike(f"%{search_query}%")).all()
    else:
        all_students = Student.query.all()
    
    return render_template('students.html', students=all_students)

@app.route('/students/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.department = request.form['department']
        student.reg_no = request.form['reg_no']
        student.city = request.form['city']
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('update_student.html', student=student)

@app.route('/students/delete/<int:id>', methods=['GET'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

if __name__ == '__main__':
    # Ensure the instance folder exists
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    
    # Create the database and tables
    with app.app_context():
        db.create_all()
    
    # Run the Flask app
    app.run(debug=True)