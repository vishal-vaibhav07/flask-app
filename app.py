from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///college.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)
#class for the database table
class College(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    reg_no = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method =='POST':
        title = request.form['title']
        desc = request.form['desc']
        reg_no = request.form['reg_no']
        college = College(title=title, desc=desc, reg_no=reg_no)
        db.session.add(college)
        db.session.commit()
        return redirect('/')
    allstu= College.query.all()
    print(allstu)
    return render_template('index.html', allstu=allstu)
    
@app.route('/show')
def products():
    allstu= College.query.all() 
    print(allstu)
    return 'This Web Appplication'
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    college = College.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        college.title = request.form['title']
        college.desc = request.form['desc']
        college.reg_no = request.form['reg_no']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', college=college)

@app.route('/delete/<int:sno>')
def delete(sno):
    allstu= College.query.filter_by(sno=sno).first()
    db.session.delete(allstu)
    db.session.commit()
    return redirect('/')
@app.route('/about')
def about():
    #allstu= College.query.all()
    #print(allstu)
    return render_template('about.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = College.query.filter(
        (College.title.ilike(f"%{query}%")) | (College.reg_no.ilike(f"%{query}%"))
    ).all()
    return render_template('index.html', allstu=results, search_query=query)

if __name__ == '__main__':
    app.run(debug=True, port=7000)