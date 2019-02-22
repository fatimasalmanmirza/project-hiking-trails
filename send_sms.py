# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from model import connect_to_db, db, User
from flask import Flask
from server import get_trail
import os
# import schedule
# import time






def send_msg():
	"""Sending trail recommendation every week."""


	account_sid = os.environ["account_sid"]
	auth_token = os.environ["auth_token"]
	users = User.query.all()
	for user in users:
		if user.phone_number is None:
			return "phone number does not exist {}".format(user.user_id)
		if user.location is None:
			return "location not found {}".format(user.user_id)

		user_phonenumber = user.phone_number
		user_location = user.location

	 
		# Your Account Sid and Auth Token from twilio.com/console
		test_sid = 'ACa07eecf8707d51cbb03d2353c182a433'
		test_auth_token = '0e013261e0966370cfa1d5eb47cc2aab'

		test = False

		if test:
			client = Client(test_sid, test_auth_token)
		else:
			client = Client(account_sid, auth_token)

		message = client.messages \
		                .create(
		                    	body="Hi Hike every weekend recommends you this trail for your weekend\n"+get_trail(user_location),
		                    	from_='+13347317307',
		                    	to=user_phonenumber
		                 )

		if message.sid is not None:
			print(f'sms sent to {user_phonenumber}: {message.sid}')

	return 0

if __name__ == "__main__":

    app = Flask(__name__)

    app.debug = True

    connect_to_db(app)
    send_msg()


    # DebugToolbarExtension(app)###############################################################################
