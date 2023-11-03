import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(100))
    description = db.Column(db.String(600))

    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description
    
    def __repr__(self):
        return f"<Book {self.title}>"


# Author
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    nationality = db.Column(db.String(100))

    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality
    
    def __repr__(self):
        return f"<Author {self.name}>"


@app.route('/')
def home():
    return 'Hello World'

if __name__ == "__main__":
    app.run(debug=True)