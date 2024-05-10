#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://www.yiibai.com/flask/flask_sqlalchemy.html
from flask import Flask, render_template, redirect, flash, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("student.cfg")

db = SQLAlchemy(app)


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, address, pin):
        self.name = name
        self.city = city
        self.addr = address
        self.pin = pin


@app.route('/')
def show_all():
    return render_template('show_all.html', students=Students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if request.form['name'] and request.form['city'] and request.form['addr']:
            student = Students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))
        else:
            flash('Please enter all the fields', 'error')
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run()
