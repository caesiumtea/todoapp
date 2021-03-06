import sys
from flask import (Flask, render_template, request, jsonify, abort, redirect,
    url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://vance@localhost:5432/todoapp")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create a class to hold our todo objects and define what fields it will have
class Todo(db.Model):
    __tablename__ = "todos"  # overwrite default table name, which would be todo
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # this just changes how objects display in interpreter, for debugging
    def __repr__(self):
        return f"<Todo {self.id}: {self.info}>"

# no longer using db.create_all() here now that migrations are set up

# route handler for index (root) page of site
@app.route("/", methods=["GET", "POST", "DELETE"])
def index():
    # render_template uses a template engine to pass the data to the view
    # and have it dynamically populate the index page
    return render_template("index.html", data=Todo.query.order_by('id').all())

# route handler for when user creates a new todo
@app.route("/todos/create", methods=["POST"])
def create_todo():
    # must define response here so that it persists after closing session
    response = {}
    error = False
    try:
        # read JSON data given by Fetch, instantiate new object with that data,
        # add to response so it can be passed back to view, and finally
        # persist new object to database
        newinfo = request.get_json()["info"]
        newtodo = Todo(info=newinfo, completed=False)
        db.session.add(newtodo)
        db.session.commit()
        #populate the response body
        response["id"] = newtodo.id
        response["info"] = newtodo.info
        response["completed"] = newtodo.completed
    except:
        # if the commit doesn't succeed, print error and roll back session
        # to protect against unexpected database states
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()  # always close connection when done!
    if error:
        abort(400)  # have the view show an error if commit failed
    else:
        # if commit succeeded, then return JSON that the view
        # can use to update list with new item
        #response['id'] = Todo.query.order_by(db.desc('id')).first().id
        return jsonify(response)


@app.route("/todos/<todo_id>/set-complete", methods=["POST"])
def set_complete(todo_id):
    error = False
    try:
        newState = request.get_json()["completed"]
        item = Todo.query.get(todo_id)
        item.completed = newState
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for("index"))

@app.route("/todos/<todo_id>/delete", methods=["DELETE"])
def delete(todo_id):
    error = False
    try:
        item = Todo.query.get(todo_id)
        db.session.delete(item)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return redirect(url_for("index"), 
            response=jsonify({'success': True}))