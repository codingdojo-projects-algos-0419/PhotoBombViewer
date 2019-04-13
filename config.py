from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import os

UPLOAD_FOLDER = './static/storage'




app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "This is my super-secret key."
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photo_bomb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)