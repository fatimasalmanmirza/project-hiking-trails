"""Models and database functions for hiking trails project."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
	"""User of Trails website"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	phone_number = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(64), nullable=False)
	location = db.Column(db.String(100), nullable=True)
	is_parking = db.Column(db.Boolean, nullable=True)
	is_restrooms = db.Column(db.Boolean, nullable=True)
	is_dogfriendly = db.Column(db.Boolean, nullable=True)
	is_kidsfriendly = db.Column(db.Boolean, nullable=True)
	is_daily = db.Column(db.Boolean, nullable=True)
	is_weekly = db.Column(db.Boolean, nullable=True)
	is_monthly = db.Column(db.Boolean, nullable=True)


	def __repr__(self):
		"""It will provide helpful representation when printed"""
		repr_str = "<User: id {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} >"
		return repr_str.format(self.user_id, self.phone_number, self.password, 
			self.location, self.is_parking, self.is_restrooms, self.is_dogfriendly,
			self.is_kidsfriendly, self.is_daily, self.is_weekly, self.is_monthly)


							
def init_app():
	# So that we can use Flask-SQLAlchemy, we'll make a Flask app.
	from flask import Flask
	app = Flask(__name__)
	connect_to_db(app)

# 	connect_to_db(app)
	print("Connected to DB.")

def connect_to_db(app):

	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hikingtrails'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)


if __name__ == "__main__":
		
		
	init_app()	
