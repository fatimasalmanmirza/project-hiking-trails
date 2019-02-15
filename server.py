from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Preference
from flask_wtf import FlaskForm
import requests
from wtforms import StringField, SelectField, SubmitField, BooleanField, PasswordField, validators, Form
import os


class PreferenceForm(FlaskForm):
	location = StringField('location')
	parking = BooleanField('Parking')
	restrooms = BooleanField('Restrooms')
	dogfriendly = BooleanField('Dog Friendly Trail')
	kidsfriendly = BooleanField('Good for kids')
	daily = BooleanField('Receive trail recommendation daily')
	weekly = BooleanField('Receive trail recommendation weekly')
	monthly = BooleanField('Receive trail recommendation monthly')

	submit = SubmitField("Lets Hike!!!!!")

class UserForm(FlaskForm):
	phonenumber = StringField('phone number')
	password = PasswordField('password')
	
	submit = SubmitField("Signup for Hike")	

	

app = Flask(__name__)




app.secret_key = os.environ["secret_key"]
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
	form = UserForm()


	return render_template("homepage.html", form=form)

# @app.route('/', methods=['POST'])
# def signup_user():
# 	request.args.get('')

@app.route('/login',methods=['GET','POST'])
def user_login():
	if request.method == 'GET':

		form = UserForm(request.form)

		return render_template("login.html", form=form)
	else:
		form = UserForm(request.form)	

		old_user = User.query.filter_by(phone_number=form.phonenumber.data).first()

		if not old_user:
			flash("No such user")
			return redirect("/")
		if old_user.password != form.password.data:
	 		flash("Incorrect password")
	 		return redirect("/")


		session["user_id"] = old_user.user_id
		return redirect("/userprofile")
		flash("logged in")



@app.route('/',methods=['POST'])
def user_signup():

		form = UserForm(request.form)
		new_user = User(phone_number=form.phonenumber.data, password=form.password.data )
		db.session.add(new_user)
		db.session.commit()
		session["user_id"] = new_user.user_id
		flash("user has been registered")
		return redirect("/preference")


@app.route("/preference", methods=['GET','POST'])
def preference():
	if request.method == 'GET':
		# display form
		form = PreferenceForm()

		return render_template("Preference.html", form=form)

	else:
		# save prefdata
		form = PreferenceForm(request.form)
		new_preferences = Preference(user_id= session["user_id"], location=form.location.data, is_parking=form.parking.data,
		is_restrooms=form.restrooms.data, is_dogfriendly=form.dogfriendly.data, is_kidsfriendly=form.kidsfriendly.data,
		is_daily=form.daily.data, is_weekly=form.weekly.data, is_monthly=form.monthly.data )

		db.session.add(new_preferences)
		db.session.commit()

		flash("preferences added to data base")
		return "data has been added"


@app.route("/userprofile")
def user_profile():
	user = User.query.get(session["user_id"])
	user_phonenumber = user.phone_number
	
	user_preferences = user.preferences


	return render_template("userprofile.html", user_phonenumber=user_phonenumber, user_preferences=user_preferences)


	



if __name__ == "__main__":

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(host="0.0.0.0", port=6001)

