import time
from flask import Flask, request, jsonify
from flask_cors import CORS
# from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_restful import Resource, Api, abort, reqparse
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import os

app = Flask(__name__)
CORS(app)

# api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://myuser:xxxx@localhost/testdb"
db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

# db.drop_all()
# db.create_all()
# db.session.add(User("mackenzie", "testemail", "123"))
# db.session.commit()
# users = User.query.all()
# print(users)



@app.route('/', methods=["GET", "POST"])
def home():
    return jsonify({"message": "testing 1,2,3"})


@app.route('/users', methods=["GET", "POST"])
def user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = User(username=data['username'], email=data['email'], password=data['password'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"user {new_user.username} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        # db.session.add(User("mackenzie", "testemail", "123"))
        # db.session.commit()
        users = User.query.all()
        results = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password
            } for user in users]

        return {"count": len(results), "users": results}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}



if __name__ == '__main__':
    app.run(debug=True) #change to False when in production level