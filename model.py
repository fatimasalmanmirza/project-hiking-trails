"""Models and database functions for hiking trails project."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
	"""information of User"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	phone_number = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(64), nullable=False)
	location = db.Column(db.String(100), nullable=True)

	trails = db.relationship("Trail", secondary="favorites", backref="users")

	def __repr__(self):
		"""It will provide helpful representation when printed"""
		repr_str = "<User: id {}, {}, {}, {} >"
		return repr_str.format(self.user_id, self.phone_number, self.password, 
			self.location)

class Trail(db.Model):
	"""Information of trails"""
	__tablename__ = "trails"
	trail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	trail_name = db.Column(db.String(50), nullable=True)
	trail_image = db.Column(db.String(1000), nullable=True)
	trail_google_direction = db.Column(db.String(1000), nullable=True)
	trail_yelp_link = db.Column(db.String(1000), nullable=True)


	def __repr__(self):
		repr_str = "<Trail: {}, {}, {}, {}, {} >"
		return repr_str.format(self.trail_id, self.trail_name, self.trail_image,
			self.trail_google_direction, self.trail_yelp_link)

class Favorites(db.Model):
	__tablename__ = "favorites"
	favorite_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
	trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'), index=True)

	#Define relationship to user
	user = db.relationship("User",
							backref=db.backref("favorites", order_by=favorite_id))
	#Define relationship to trail
	trail = db.relationship("Trail",
							backref=db.backref("favorites", order_by=favorite_id))


	def __repr__(self):
		repr_str = "<Favorites: favorite_id{}, user_id{}, trail_id{} >"
		return repr_str.format(self.favorite_id, self.user_id, self.trail_id)
							
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
