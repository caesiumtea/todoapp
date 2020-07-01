from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#route handler for index (root) page of site
@app.route('/')
def index():
    return render_template('index.html', data=[{
        "info":"Item 1"
        }, {
        "info":"Item 2"
        }, {
        "info":"Item 3"
    }]) #this is dummy data currently, will replace with a list of objects
        #pulled from database by SQLAlchemy