from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class user(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password


class post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	created = db.Column(db.DateTime, default=datetime.now)
	title = db.Column(db.String(200), nullable=False)
	body = db.Column(db.Text, nullable=False)

	def __init__(self, author_id, title, body):
		self.author_id = author_id
		self.title = title
		self.body = body