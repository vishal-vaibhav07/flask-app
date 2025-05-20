from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    reg_no = db.Column(db.String(100), unique=True)
    city = db.Column(db.String(100))

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    employee_id = db.Column(db.String(100), unique=True)
    city = db.Column(db.String(100))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return render_template('index.html')
    else:
        return "<h2>Invalid credentials. <a href='/'>Try again</a></h2>"
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/fees')
def fees():
    course = request.args.get('course')
    # Use 'course' to display the relevant fee details in your template
    return render_template('fees.html', course=course)

@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        reg_no = request.form['reg_no']
        city = request.form['city']

        # Check for duplicate reg_no
        existing_student = Student.query.filter_by(reg_no=reg_no).first()
        if existing_student:
            flash('⚠️ A student with this registration number already exists!', 'danger')
            return redirect(url_for('students'))

        new_student = Student(name=name, department=department, reg_no=reg_no, city=city)
        db.session.add(new_student)
        db.session.commit()
        flash('✅ Student added successfully!', 'success')
        return redirect(url_for('students'))

    search_query = request.args.get('search')
    if search_query:
        students = Student.query.filter(Student.name.like(f"%{search_query}%")).all()
    else:
        students = Student.query.all()

    return render_template('students.html', students=students)

#Faculty
@app.route('/faculty', methods=['GET', 'POST'])
def faculty():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        employee_id = request.form['employee_id']
        city = request.form['city']

        # Check for duplicate reg_no
        existing_faculty = Faculty.query.filter_by(employee_id=employee_id).first()
        if existing_faculty:
            flash('⚠️ A faculty with this employeeID already exists!', 'danger')
            return redirect(url_for('faculty'))

        new_faculty = Faculty(name=name, department=department, employee_id=employee_id, city=city)
        db.session.add(new_faculty)
        db.session.commit()
        flash('✅ Faculty added successfully!', 'success')
        return redirect(url_for('faculty'))

    search_query = request.args.get('search')
    if search_query:
        faculty = Faculty.query.filter(Faculty.name.like(f"%{search_query}%")).all()
    else:
        faculty = Faculty.query.all()

    return render_template('faculty.html', faculty=faculty)

@app.route('/students/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('🗑️ Student deleted!', 'warning')
    return redirect(url_for('students'))

@app.route('/students/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.department = request.form['department']
        student.city = request.form['city']
        db.session.commit()
        flash('✏️ Student updated successfully!', 'info')
        return redirect(url_for('students'))
    return render_template('update_student.html', student=student)
#Update Faculty
@app.route('/faculty/update/<int:id>', methods=['GET', 'POST'])
def update_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    if request.method == 'POST':
        faculty.name = request.form['name']
        faculty.department = request.form['department']
        faculty.email = request.form['email']
        faculty.city = request.form['city']
        db.session.commit()
        flash("Faculty updated successfully!", "success")  # green alert
        return redirect('/faculty')
    return render_template('update_faculty.html', faculty=faculty)
#delete faculty
@app.route('/faculty/delete/<int:id>')
def delete_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    db.session.delete(faculty)
    db.session.commit()
    flash('Faculty deleted!', 'warning')
    return redirect(url_for('faculty'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
