from config import db, bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import re
from flask import session
import os.path


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Users(id ='%s', first_name ='%s', last_name ='%s', email='%s')" % \
               (self.id, self.first_name, self.last_name, self.email)

    @classmethod
    def validate(cls, form):

        errors = []
        if len(form['first_name']) < 2:
            errors.append("First name must be greater than 2 characters")
        if len(form['last_name']) < 2:
            errors.append("Last name must be greater than 2 characters")
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Email address format invalid")

        if 'user_id' not in session:
            existing_email = cls.query.filter_by(email=form['email']).first()
            if existing_email:
                errors.append("Email address already in use")

            if len(form['password']) < 4:
                errors.append("Password must be at least 4 characters long")

            if form['password'] != form['password_confirm']:
                errors.append("Password mis-match")
        return errors

    @classmethod
    def create(cls, form):
        print(f"PASS: {form['password']}")
        pw_hash = bcrypt.generate_password_hash(form['password'])
        user = cls(first_name=form['first_name'],
                   last_name=form['last_name'],
                   email=form['email'],
                   password=pw_hash
                   )
        db.session.add(user)
        db.session.commit()
        return user.id

    @classmethod
    def login_validate(cls, form):
        user = cls.query.filter_by(email=form['login_email']).first()
        if user:
            if bcrypt.check_password_hash(user.password, form['login_password']):
                return True, user.id
        return False, "Email or bad password"


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    file_path = db.Column(db.String(200))
    file_name = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_by = db.relationship('Users', foreign_keys=[user_id], backref='user_photos')

    def __repr__(self):
        return "Photos(id ='%s', user_id ='%s', description ='%s', file_path = '%s')" % \
               (self.id, self.user_id, self.description, self.file_path)

    @classmethod
    def add_to_db(cls, filename, user_id):
        photo = cls(file_name=filename,
                    user_id=user_id
                    )
        db.session.add(photo)
        db.session.commit()
        return photo.id


