import time
from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL
# from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
# from flask_restful import Resource, Api, abort, reqparse
from flask_marshmallow import Marshmallow
# from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import os

app = Flask(__name__)
CORS(app)


# api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://myuser:xxxx@localhost/testdb"
db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow(app)



class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(24))
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64))
    tasks = db.relationship('Task', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'name',
            'email',
            'password'
        )

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    date = db.Column(db.Date)
    body = db.Column(db.Text)

    def __init__(self, user_id, category_id, goal_id, date, body):
        self.user_id = user_id
        self.category_id = category_id
        self.goal_id = goal_id
        self.date = date
        self.body = body

    def __repr__(self):
        return '<Task %r>' % self.id

class TaskSchema(ma.Schema):
    class Meta:
            fields = (
                'id',
                'user_id',
                'category_id',
                'goal_id',
                'date',
                'body'
            )

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(24))
    tasks = db.relationship('Task', backref='category', lazy=True)
    goals = db.relationship('Goal', backref='category', lazy=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Category %r>' % self.title

class CategorySchema(ma.Schema):
    class Meta:
            fields = (
                'id',
                'title',
            )

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

class Goal(db.Model):
    __tablename__ = 'goal'
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    tag = db.Column(db.String(24))
    description = db.Column(db.String(64))
    weekly_freq = db.Column(db.Integer)
    

    def __init__(self, user_id, category_id, tag, description, weekly_freq):
        self.user_id = user_id
        self.category_id = category_id
        self.tag = tag
        self.description = description
        self.weekly_freq = weekly_freq

    def __repr__(self):
        return '<Goal %r>' % self.tag

class GoalSchema(ma.Schema):
    class Meta:
        fields = (
            'user_id',
            'category_id',
            'tag',
            'description',
            'weekly_freq'
        )

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)

# db.drop_all()
# db.create_all()
# db.session.add(User("mackenzie", "testemail", "123"))
# db.session.commit()
# users = User.query.all()
# print(users)

migrate = Migrate(app, db)

@app.route('/', methods=["GET", "POST"])
def home():
    return jsonify({"message": "testing 1,2,3"})

#USERS 
@app.route('/users', methods=["GET", "POST"])
def user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = User(name=data['name'], email=data['email'], password=data['password'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"user {new_user.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        users = User.query.all()
        results = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password
            } for user in users]

        return {"count": len(results), "users": results}
    
    # elif request.method == 'PUT':
    #     data = request.get_json()
    #     car.name = data['name']
    #     car.model = data['model']
    #     car.doors = data['doors']
    #     db.session.add(car)
    #     db.session.commit()
    #     return {"message": f"car {car.name} successfully updated"}


#TASKS
@app.route('/tasks', methods=["GET", "POST"])
def task():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_task = Task(user_id=data['user_id'], category_id=data['category_id'], goal_id=data['goal_id'], date=data['date'], body=data['body'])
            db.session.add(new_task)
            db.session.commit()
            return {"message": f"task {new_task.id} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        tasks = Task.query.all()
        results = [
            {
                "id": task.id,
                "user_id": task.user_id,
                "user": task.user_id.name,
                "category_id": task.category_id,
                "goal_id": task.goal_id,
                "date": task.date,
                "body": task.body
            } for task in tasks]

        return {"count": len(results), "tasks": results}

@app.route('/tasks/<task_id>', methods=["PUT", "DELETE"])
def handle_task(task_id): 
    task = TaskModel.query.get_or_404(task_id)  

    if request.method == 'PUT':
        data = request.get_json()
        task.category_id = data['category_id']
        task.goal_id = data['goal_id']
        task.date = data['date']
        task.body = data['body']
        db.session.add(task)
        db.session.commit()
        return {"message": f"task {task.id} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return {"message": f"Task {task.id} successfully deleted."}

#CATEGORIES
@app.route('/categories', methods=["GET", "POST", "PUT"])
def category():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_category = Category(title=data['title'])
            db.session.add(new_category)
            db.session.commit()
            return {"message": f"category {new_category.title} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        categories = Category.query.all()
        results = [
            {
                "id": category.id,
                "title": category.title,
            } for category in categories]

        return {"count": len(results), "categories": results}
    
@app.route('/categories/<category_id>', methods=["PUT"])
def handle_category(category_id): 
    category = CategoryModel.query.get_or_404(category_id)    
    
    if request.method == 'PUT':
        data = request.get_json()
        category.title = data['title']
        db.session.add(category)
        db.session.commit()
        return {"message": f"category {category.title} successfully updated"}



#GOALS
@app.route('/goals', methods=["GET", "POST"])
def goal():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_goal = Task(user_id=data['user_id'], category_id=data['category_id'], tag=data['tag'], description=data['description'], weekly_freq=data['weekly_freq'])
            db.session.add(new_goal)
            db.session.commit()
            return {"message": f"goal {new_goal.tag} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        goals = Goal.query.all()
        results = [
            {
                "id": goal.id,
                "user_id": goal.user_id,
                "category_id": goal.category_id,
                "tag": goal.tag,
                "description": goal.description,
                "weekly_freq": goal.weekly_freq
            } for goal in goals]

        return {"count": len(results), "goals": results}

@app.route('/goals/<goal_id>', methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id): 
    goal = GoalModel.query.get_or_404(goal_id)

    if request.method == 'GET':
        response = {
                "user_id": goal.user_id,
                "category_id": goal.category_id,
                "tag": goal.tag,
                "description": goal.description,
                "weekly_freq": goal.weekly_freq
            }

        return {"message": success, "goal": response}
    elif request.method == 'PUT':
        data = request.get_json()
        goal.category_id = data['category_id']
        goal.tag = data['tag']
        goal.description = data['description']
        goal.weekly_freq = data['weekly_freq']
        db.session.add(task)
        db.session.commit()
        return {"message": f"goal {goal.tag} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return {"message": f"Goal {goal.tag} successfully deleted."}


@app.route('/time')
def get_current_time():
    return {'time': time.time()}



if __name__ == '__main__':
    app.run(debug=True) #change to False when in production level