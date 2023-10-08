from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for


from werkzeug.security import generate_password_hash, check_password_hash 

from flask_login import login_required, current_user

from .models import Note, User

from . import db

import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <= 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/reset-password', methods=['GET', 'POST'])

def reset():
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, current_password):
            flash('Incorrect email or password!', 'error')
            return redirect(url_for('views.reset'))

        if new_password != confirm_password:
            flash('New passwords do not match!', 'error')
            return redirect(url_for('views.reset'))

        user.password = generate_password_hash(new_password, method='scrypt')
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('views.home'))

    return render_template('reset-password.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()


    return jsonify({})