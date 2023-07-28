from flask_app import app
from flask import render_template, redirect,request,session,flash
import re
from flask_app.models.user import User
from flask_app.models.game import Game
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#route to render index page
@app.route("/")
def index():
    return render_template("index.html")

#route to render sign up form
@app.route("/signupform")
def signupform():
    return render_template("signupform.html")

#route to render login form
@app.route("/loginform")
def loginform():
    return render_template("loginform.html")

#the route used to manipulate the data and call to insert it into the database
@app.route('/register', methods=['POST'])
def create_user():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not User.validate_user(request.form):
        return redirect('/signupform')

    if user_in_db:
        flash('Email already exists. Please Log In')
        return redirect('/')
    passhash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'fname' : request.form['fname'],
        'lname' : request.form['lname'],
        'email' : request.form['email'],
        'password' : passhash
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    session['username'] = data['fname']
    return redirect('/dashboard')

#the route used to log in
@app.route('/login', methods=['POST'])
def login():

    data = {'email': request.form['email']}

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash('Invalid Email or Password')
        return redirect('/loginform')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email or Password')
        return redirect('/loginform')
    
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.first_name

    return redirect('/dashboard')

#The route used to render the dashboard page
@app.route('/dashboard')
def logged_in():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template('dashboard.html',
                            username = session['username'],
                            user_id = session['user_id'], games = Game.get_all())

#a route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
