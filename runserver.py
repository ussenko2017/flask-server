# -*- coding: utf-8 -*-
"""
This script runs the Flask application using a development server.
"""

from flask import render_template,g
from Flask import app
import flask,myFunc
from datetime import datetime



import flask_login

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    db = myFunc.createTables(myFunc.DBName)
    users = db.select(db.SELECT_TYPE_STANDARD, myFunc.USER_TABLE, 0)
    if email not in users:
        return

    user = User()
    user.id = email

    return user


@login_manager.request_loader
def request_loader(request):
    db = myFunc.createTables(myFunc.DBName)
    users = db.select(db.SELECT_TYPE_STANDARD, myFunc.USER_TABLE, 0)
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user




#users = {'foo@bar.tld': {'password': 'secret'}}
spisok = []
dict = dict(header='Августовская конференция',text='На ежегодной августовской конференции педагогических работников образования, Политехнический колледж Астаны получил грант акима города Астаны как лучшая организация Технического и профессионального образования. Асет Исекешев вручил сертификат в размере 10 млн. тенге.')
spisok.append(dict)
spisok.append(dict)
spisok.append(dict)
spisok.append(dict)
spisok.append(dict)
@app.route('/')
def home():
    try:
        user = flask_login.current_user.id
    except:
        user = 'null'
    return render_template('index.html',spisok=spisok,user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():

        db = myFunc.createTables(myFunc.DBName)
        users = db.select(db.SELECT_TYPE_STANDARD, myFunc.USER_TABLE, 0)
        email = flask.request.form['email']
        if email in users:
            if flask.request.form['password'] == users[email]['password']:
                user = User()
                user.id = email
                flask_login.login_user(user)

                return flask.redirect(flask.url_for('home'))

        return flask.redirect(flask.url_for('home'))

@app.route('/protected')
@flask_login.login_required
def protected():
    return flask.redirect(flask.url_for(''))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    g.user = 'Гость'
    return flask.redirect(flask.url_for('home'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
@app.route('/reg',methods=['GET', 'POST'])
def reg():
        db = myFunc.createTables(myFunc.DBName)
        users = db.select(db.SELECT_TYPE_STANDARD, myFunc.USER_TABLE, 0)
        email = flask.request.form['email']
        password = flask.request.form['password']

        if email not in users:
            myFunc.addUser([email,password,myFunc.getDate()],email)
            g.user = email
            return flask.redirect(flask.url_for('home'))

        return flask.redirect(flask.url_for('home'))








@app.route('/balls',methods=['GET','POST'])
def showball():
    db = myFunc.createTables(myFunc.DBName)
    balls = db.select(db.SELECT_TYPE_STANDARD, myFunc.BALL_TABLE, 0)
    students = db.select(db.SELECT_TYPE_STANDARD, myFunc.STUDENT_TABLE, 0)
    predmets = db.select(db.SELECT_TYPE_STANDARD, myFunc.PREDMET_TABLE, 0)

    return render_template(
        'data/ball.html',
        balls=balls,
        students=students,
        predmets=predmets,
        year=datetime.now().year
    )

@app.route('/journal',methods=['GET','POST'])
def showjournal():
    db = myFunc.createTables(myFunc.DBName)
    balls = db.select(db.SELECT_TYPE_STANDARD, myFunc.BALL_TABLE, 0)
    students = db.select(db.SELECT_TYPE_STANDARD, myFunc.STUDENT_TABLE, 0)
    predmets = db.select(db.SELECT_TYPE_STANDARD, myFunc.PREDMET_TABLE, 0)

    return render_template(
        'data/journal.html',
        year=datetime.now().year,
        predmets=predmets,
        balls=balls,
        students=students
    )



@app.route('/students',methods=['GET','POST'])
def showstudent():
    db = myFunc.createTables(myFunc.DBName)
    students = db.select(db.SELECT_TYPE_STANDARD,myFunc.STUDENT_TABLE,0)
    otdels = db.select(db.SELECT_TYPE_STANDARD,myFunc.OTDEL_TABLE,0)

    return render_template(
        'data/student.html',
        students=students,
        otdels=otdels,
        year=datetime.now().year
    )

@app.route('/predmets',methods=['GET','POST'])
def showpredmet():
    db = myFunc.createTables(myFunc.DBName)
    predmets = db.select(db.SELECT_TYPE_STANDARD,myFunc.PREDMET_TABLE,0)
    return render_template(
        'data/predmet.html',
        predmets=predmets,
        year=datetime.now().year
        #
    )

@app.route('/otdels',methods=['GET','POST'])
def showotdel():
    db = myFunc.createTables(myFunc.DBName)
    otdels = db.select(db.SELECT_TYPE_STANDARD, myFunc.OTDEL_TABLE, 0)
    return render_template(
        'data/otdel.html',
        otdels=otdels,
        year=datetime.now().year
    )


@app.route('/autoadd',methods=['GET','POST'])
def autoadd():
    myFunc.autoadd()
    return 'done'



@app.route('/api/v1/add/',methods=['GET','POST'])
def add():
    db = myFunc.createTables(myFunc.DBName)
    tablename = flask.request.values.get('tablename')

    if tablename == myFunc.STUDENT_TABLE:
        firstname = flask.request.values.get(myFunc.FIRSTNAME_FIELD)
        lastname = flask.request.values.get(myFunc.LASTNAME_FIELD)
        patr = flask.request.values.get(myFunc.PATR_FIELD)
        number = flask.request.values.get(myFunc.NUMBER_FIELD)
        otdel_id = flask.request.values.get(myFunc.OTDEL_ID_FIELD)


        if firstname != '' and lastname != '' and number != '' and otdel_id != '':
            db.addRow(tablename,[firstname,lastname,patr,number,otdel_id,myFunc.getDate()])
            return  flask.jsonify({'ok':200})
    elif tablename == myFunc.OTDEL_TABLE:
        name = flask.request.values.get(myFunc.NAME_FIELD)
        if name != '':
            db.addRow(tablename,[name,myFunc.getDate()])
            return  flask.jsonify({'ok':200})

    elif tablename == myFunc.PREDMET_TABLE:
        name = flask.request.values.get(myFunc.NAME_FIELD)
        kolvo_chasov = flask.request.values.get(myFunc.KOLVO_CHASOV_FIELD)
        if name != '' and kolvo_chasov != '':
            db.addRow(tablename,[name,kolvo_chasov,myFunc.getDate()])
            return  flask.jsonify({'ok':200})

    elif tablename == myFunc.BALL_TABLE:
        ball = flask.request.values.get(myFunc.BALL_FIELD)
        predmet_id = flask.request.values.get(myFunc.STUDENT_ID_FIELD)
        student_id = flask.request.values.get(myFunc.PREDMET_ID_FIELD)
        if ball != '' and predmet_id != '' and student_id != '':
            db.addRow(tablename,[ball,predmet_id,student_id,myFunc.getDate()])
            return  flask.jsonify({'ok':200})


    return flask.jsonify({'error':400})

if __name__ == '__main__':
    app.run()

