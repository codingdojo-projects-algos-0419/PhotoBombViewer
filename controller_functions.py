from flask import Flask, render_template, redirect, request, session, \
    flash, send_from_directory, url_for
from models import Users, Photos
from config import db, app
from flask_sqlalchemy import SQLAlchemy

import os
from werkzeug.utils import secure_filename

import PIL
from PIL import Image


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'png'])
CARDS_PER_ROW = 4


def show_upload_page():
    print(f"ROUTE: show_upload_page")
    return render_template("upload.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    user_id = str(session['user_id'])
    store_file_path = "./static/storage/" + user_id
    if not os.path.exists(store_file_path):
        os.makedirs(store_file_path)

    print(f"ROUTE: upload_file")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(f"Uploading {file}")
            filename = secure_filename(file.filename)
            file.save(os.path.join(store_file_path, filename))
            flash('File(s) successfully uploaded')
            Photos.add_to_db(filename, store_file_path, user_id)
            return redirect(url_for("show_dashboard"))


def uploaded_file(filename):
    print(f"ROUTE: uploaded_file")
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def index():
    print(f"ROUTE: index")
    return render_template("index.html")


def register():
    print(f"ROUTE: register")
    return render_template("register.html")


def show_login_page():
    print(f"ROUTE: show_login_page")
    return render_template("login.html")


def login():
    print(f"ROUTE: login: {request.form}")
    valid, response = Users.login_validate(request.form)
    print(f"Valid: {valid} Response= {response}")

    if not valid:
        flash(response)
        return redirect('/login')
    session['user_id'] = response
    return redirect("/dashboard")


def show_dashboard():
    print(f"ROUTE: show_dashboard")
    if 'user_id' not in session:
        return redirect('/')

    current_user = Users.query.get(session['user_id'])
    current_user_photos = current_user.user_photos
    print(f"PHOTOS: {current_user_photos}")
    return render_template("dashboard.html", user=current_user, photos=current_user_photos)


def process_new_user():
    print(f"ROUTE: process_new_user REQUEST: {request.form}")
    errors = Users.validate(request.form)
    if errors:
        print(f" FOUND ERRORS: {errors}")
        for error in errors:
            flash(error)
        return redirect('/register')

    user_id = Users.create(request.form)
    session['user_id'] = user_id
    return redirect("/dashboard")


def users_logout():
    print(f"ROUTE: logout")
    session.clear()
    return redirect('/')


def show_edit_page(id):
    print(f"ROUTE: show_edit_page")
    current_photo = Photos.query.get(id)
    current_user = Users.query.get(session['user_id'])
    return render_template("edit_photo.html", user=current_user, photo=current_photo)


def update_photo_info(id):
    print(f"ROUTE: update_photo_info")
    # print(f"REQUEST FORM: {request.form}")
    current_user = Users.query.get(session['user_id'])

    photo = Photos.query.get(id)

    store_path = photo.file_path + '/' + photo.file_name
    store_path_new = photo.file_path + '/' + request.form['photo_file_name']
    # print(f"Update filepath = {store_path}")

    if photo.file_name != request.form['photo_file_name']:
        print(f"Update filename")
        photo.file_name = request.form['photo_file_name']
        print(f"Renaming file from {store_path} to {store_path_new}")
        os.rename(store_path, store_path_new)

    if photo.description != request.form['photo_description']:
        print(f"Update description")
        photo.description = request.form['photo_description']

    # if photo.create_at != request.form['photo_create_date']:
    #     print(f"Update create_date")
    #     photo.create_at = request.form['photo_create_date']

    # ret_id = str(photo.id)
    db.session.commit()

    return redirect(url_for("show_dashboard"))


def delete_photo(id):
    print(f"ROUTE: delete_photo")
    # print(f"REQUEST FORM: {request.form}")
    current_user = Users.query.get(session['user_id'])

    photo = Photos.query.get(id)

    store_path = photo.file_path + '/' + photo.file_name
    print(f"Removing file {store_path}")

    try:
        if os.path.exists(store_path):
            os.remove(store_path)
        else:
            raise IOError(f"Unable to find file: {store_path}")
    except IOError as ex:
        raise ex

    db.session.delete(photo)
    db.session.commit()

    return redirect(url_for("show_dashboard"))



