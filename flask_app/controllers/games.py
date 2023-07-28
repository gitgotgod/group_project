from flask_app import app
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.game import Game

#route to render new game page
@app.route("/new")
def new():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template("newgame.html")

#route to save a game
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
    return  redirect('/dashboard')

#route to render edit game page
@app.route("/edit/<id>")
def edit(id):
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    return render_template("editgames.html", game = Game.get_one({"id" : id}))

#route to delete game
@app.route("/delete/<id>")
def delete(id):
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    Game.destroy({"id" : id})
    return redirect("/dashboard")

#route to edit a game
@app.route("/editgame", methods=["POST"])
def update():
    data = {
        'id': request.form['id'],
        'hometeam': request.form['hometeam'],
        'homescore': request.form['homescore'],
        'awayteam': request.form['awayteam'],
        'awayscore': request.form['awayscore']
    }
    Game.edit(data)
    return redirect("/dashboard")

#route to edit view page
@app.route("/view/<id>")
def viewOne(id):
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    return render_template("view.html", game = Game.get_one({'id' : id}))
