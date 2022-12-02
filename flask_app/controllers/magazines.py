from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.magazine import Magazine
from flask_app.models.user import User


@app.route('/show/<int:id>')
def showMagazine(id):
    if 'user' not in session:
        return redirect('/logout')

    data = {
        'magazine_id': id
    }
    currentMagazine = Magazine.getMagazineByID(data)
    return render_template("showMagazine.html", currentMagazine = currentMagazine)


@app.route('/addMagazine')
def formToAdd():
    if 'user' not in session:
        return redirect('/logout')
    return render_template("createMagazine.html")

@app.route('/magazineAdd', methods = ['POST'])
def addMagazine():
    if not Magazine.validata_magazine(request.form):
        flash("Please, fill in the fields correctly", 'magazineCreate')
        return redirect(request.referrer)
    data = {
        'tittle': request.form['tittle'],
        'description': request.form['description'],
        'user_id': session['user']
    }
    Magazine.addMagazine(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def deleteMagazine(id): 
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'magazine_id': id
    }
    currentMagazine = Magazine.getMagazineByID(data)
    if not session['user'] == currentMagazine['user_id']:
        return render_template("404Error.html")
    Magazine.destroyMagazine(data)
    return redirect(request.referrer)

@app.route('/subscribe/<int:id>')
def subscribe(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'magazine_id': id,
        'user_id': session['user']
    }
    Magazine.subscribeMagazine(data)
    return redirect(request.referrer)

@app.route('/unsubscribe/<int:id>')
def unsubscribe(id):
    if 'user' not in session:
        return redirect('/logout')    
    data = {
        'magazine_id': id,
        'user_id': session['user']
    }
    Magazine.unsubscribeMagazine(data)
    return redirect(request.referrer)

