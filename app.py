from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list=Todo.query.all()
    print(todo_list)
    return render_template('index.html',todo_list=todo_list)

@app.route("/add",methods=["POST"])
def add():
    title=request.form.get("title")
    new_todo=Todo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
   todo=Todo.query.filter_by(id=todo_id).first()
   db.session.delete(todo)
   db.session.commit()
   return redirect(url_for("index"))

@app.route('/edit/<int:todo_id>',methods=["GET","POST"])
def edit(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    if request.method == 'POST':
        title = request.form.get("title")
        try:

            num_rows_updated = Todo.query.filter_by(id=todo.id).update(dict(title=title))

            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('edit.html',todo_id=todo.id,title=todo.title)

if __name__=="__main__":
    db.create_all()

    app.run(debug=True)