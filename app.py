from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://flask-todo-app:renish@cluster0.ftdrd.mongodb.net/dbtodo?retryWrites=true&w=majority'
app.DEBUG=False
mongo = PyMongo(app)

todos = mongo.db.todos

@app.route('/')
def index():
    saved_todos=todos.find()
    return render_template('index.html',todos=saved_todos)

@app.route('/add_todo',methods=['POST'])
def add_todo():
    new_todo = request.form.get('add-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item=todos.find_one({'_id':ObjectId(oid)})
    todo_item['complete']=not todo_item['complete']
    todos.save(todo_item)
    return redirect(url_for('index'))

@app.route('/edit_todo/<oid>',methods=['POST'])
def edit_todo(oid):
    edit_item = request.form.get('edit-todo')
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    # todo_item['text'] = edit_item
    todos.update({'_id':ObjectId(oid)},{'text':edit_item,'complete': todo_item['complete']})
    # todos.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_todo/<oid>')
def delete_todo(oid):
    todos.delete_many({'_id': ObjectId(oid)})
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete':True})
    return redirect(url_for('index'))


@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))

