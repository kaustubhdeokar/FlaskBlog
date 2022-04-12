from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# three slashes after sqlite: for relative path, 4 for absolute.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.userid


@app.route("/adduser", methods=['POST', 'GET'])
def adduser():
    username = request.form.get('username')
    password = request.form.get('password')
    new_user = Users(username=username, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return 'adding user failed'


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        user = Users.query.filter_by(username=username).first()
        return f' {user.username} ' + " " + str(user.password)
    except Exception as e:
        return 'failure'


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        task_content = request.form.get('content')
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'adding task failed.'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("login.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'delete task ' + str(id) + 'failed.'


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form.get('content')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'update task ' + str(id) + 'failed.'
    else:
        return render_template("update.html", tasks=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)
