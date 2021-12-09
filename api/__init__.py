import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql_auth import (
    GraphQLAuth,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/task.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "SECRET"
app.config["ACCESS_EXP_LENGTH"] = False
# app.config["REFRESH_EXP_LENGTH"] = 300
auth = GraphQLAuth(app)


@app.route('/')
def root():
    return "<h1>Hello,</h1><p>for using api <a href='/graphql'>click here!</a></p>"
