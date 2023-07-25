from flask_app import app
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.game import Game

@app.route("/view")
def viewall():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template("allgames.html", games = Game.get_all())

@app.route("/new")
def new():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template("newgame.html")

@app.route("/savegame", methods=["POST"])
def save():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'hometeam': request.form['hometeam'],
        'homescore': request.form['homescore'],
        'awayteam': request.form['awayteam'],
        'awayscore': request.form['awayscore']
    }
    print(data)
    Game.save(data)
    return  redirect('/new')

@app.route("/edit")
def edit():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    return render_template("editgames.html", games = Game.get_all())

@app.route("/delete")
def delete():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')