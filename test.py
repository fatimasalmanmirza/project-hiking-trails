import unittest

from server import app
from model import db, connect_to_db, User, Trail, Favorites
import re

class ServerTests(unittest.TestCase):
	"""Tests for my trails site"""

	def setUp(self):
		self.client = app.test_client()
		app.config['TESTING'] = True

	def test_login(self):
		result = self.client.get("/")
		self.assertIn(
			b"Already", result.data)

	def test_login(self):
		result = self.client.get("/signup")
		self.assertIn(b"signup", result.data)


class TestUser(unittest.TestCase):
    """Ensure user can register"""


    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app)

        # Create tables and add sample data
        db.create_all()
        fati = User(phone_number='+14159106112', password ='fati', location='Fremont')
        db.session.add(fati)
        db.session.commit()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        
    def test_user_registration(self):
        """Test to see if new user can be registered"""
        with self.client:
            response = self.client.post('/signup', data={
                'phone_number': '+14159106112',
                'password': 'fati',
                'location': 'fremont'    
       		 }, follow_redirects=True)
            self.assertIn(b'user has been registered', response.data)
            user = User.query.filter_by(phone_number = "+14159106112").first()
            self.assertTrue(user.password == 'fati')

    def user_profile(self):
    	with self.client:
    		response = self.client.get('/userprofile') 
    		self.asserIn(b'Hi Hiker', response.data)

    def edit_location(self):
    	with self.client:
    		response = self.client.get('/editlocation')
    		self.asserIn(b'location', response.data)

    def show_trails(self):
    	with self.client:
    		response = self.client.get('/logout')
    		self.asserIn(b'Already', response.data)			


class FlaskTests(unittest.TestCase):
	"""Flask tests for valid and invalid login credentials and successful logout session"""
	def setUp(self):
		"""Stuff to do before every test."""

		# Get the Flask test client
		self.client = app.test_client()

		# Show Flask errors that happen during tests
		app.config['TESTING'] = True

		# Connect to test database
		connect_to_db(app)

		# Create tables and add sample data
		db.create_all()
		new_user = User(phone_number='+14159106112', password ='fati', location='Fremont')
		db.session.add(new_user)
		db.session.commit()

	def tearDown(self):
		"""Do at end of every test."""

		db.session.close()
		db.drop_all
        

	def test_login_incorrect_email(self):
    #attempt login with incorrect email credentials
		response = self.client.post('/', data={
	        'phone_number': '123',
	        'password': 'fati'
	    }, follow_redirects=True)
		self.assertTrue(re.search('No such user',
	                    response.get_data(as_text=True)))        
    # def add_fav(self):
    # 	with self.client:
    # 		response = self.client.post('/save-trails', data={
    # 			'trailImage': 'url'
    # 			'trailDir': 'abc'
    # 			'trailUrl': 'cde'
    # 			'trailName': 'regional'
    # 			}),
    # 		trail = Trail(trail_name=trailName, trail_image=img,
    #         trail_google_direction=trailDir, trail_yelp_link=trailUrl)
					
    # 		db.session.add(trail)
    # 		db.session.commit()
    # 		fav = Favorites(user_id=session["user_id"], trail_id=trail.trail_id)
    # 		db.session.add(fav)
    # 		db.session.commit()
    # 		user = User.query.filter_by(trail_name = "regional").first()
    # 		self.assertTrue(trail.trail_image='url')

if __name__== "__main__":
	unittest.main()

