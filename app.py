from flask import Flask, render_template
from config import app, db
from models import Users
import routes


if __name__ == '__main__':
    app.run(debug=True)
