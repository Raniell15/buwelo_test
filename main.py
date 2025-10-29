from flask import Flask
from flask import render_template
from flask import request
from flask import redirect,url_for
from util.db import conn

app = Flask(__name__)

@app.route("/")
def index():
    db_conn = conn()
    cur = db_conn.cursor()
    cur.execute('''SELECT first_name, last_name, address, job_title, emp_code FROM employees ORDER BY id ASC''')
    data = cur.fetchall()  
    db_conn.close()
    cur.close()
    return render_template('index.html', employees = data)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        db_conn = conn()
        cur = db_conn.cursor()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        job_title = request.form['job_title']
        cur.execute('''INSERT INTO employees (first_name, last_name, address, job_title) VALUES (%s, %s, %s, %s)''', (first_name, last_name, address, job_title))
        db_conn.commit()
        cur.close()
        db_conn.close()
        return redirect(url_for('index'))
    else:    
        return render_template('add.html')

@app.route("/edit/<emp_code>", methods=['GET', 'POST'])
def edit(emp_code):
    if request.method == "POST":
        db_conn = conn()
        cur = db_conn.cursor()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        job_title = request.form['job_title']
        cur.execute('''UPDATE employees SET first_name = %s, last_name = %s, address = %s, job_title = %s WHERE emp_code = %s''', (first_name, last_name, address, job_title,emp_code))
        db_conn.commit()
        cur.close()
        db_conn.close()
        return redirect(url_for('index'))
    else:
        db_conn = conn()
        cur = db_conn.cursor()
        cur.execute('''SELECT first_name, last_name, job_title, address FROM employees WHERE emp_code = (%s)''', (emp_code,))
        data = cur.fetchall()
        db_conn.close()
        cur.close()
        return render_template('edit.html', employee=data[0], emp_code = emp_code)

@app.route("/delete/<emp_code>")
def delete(emp_code):
    db_conn = conn()
    cur = db_conn.cursor()
    cur.execute('''DELETE FROM employees WHERE emp_code = %s ''', (emp_code,))
    db_conn.commit()
    db_conn.close()
    cur.close()
    return redirect(url_for('index'))

@app.errorhandler(404)
def notFound(error):
    return render_template("notFound.html"),404