from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://vance@localhost:5432/todoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id}: {self.info}>"

db.create_all()

#route handler for when user creates a new todo
@app.route("/todos/create", methods=["POST"])
def create_todo():
    newinfo = request.get_json()["info"]
    newtodo = Todo(info=newinfo)
    db.session.add(newtodo)
    db.session.commit()
    #return JSON that the view can use to update list with new item
    return jsonify({"info": newtodo.info})

#route handler for index (root) page of site
@app.route("/")
def index():
    return render_template("index.html", data=Todo.query.all())    