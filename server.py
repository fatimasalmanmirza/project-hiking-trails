from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User
from flask_wtf import FlaskForm
import requests
from wtforms import StringField, SelectField, SubmitField, BooleanField, PasswordField, validators, Form
import os
import random
from twilio.rest import Client
import urllib.parse


class PreferenceForm(FlaskForm):
    location = StringField('location')
    

    submit = SubmitField("Lets Hike!!!!!")


class UserForm(FlaskForm):
    phonenumber = StringField('phone number')
    password = PasswordField('password')
    submit = SubmitField("lets Hike!!")


app = Flask(__name__)


app.secret_key = os.environ["secret_key"]
map_key = os.environ["google_map_key"]
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    form = UserForm()

    return render_template("homepage.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """user login"""
    if request.method == 'GET':

        form = UserForm(request.form)

        return render_template("login.html", form=form)
    else:
        form = UserForm(request.form)

        old_user = User.query.filter_by(
            phone_number=form.phonenumber.data).first()

        if not old_user:
            flash("No such user")
            return redirect("/")
        if old_user.password != form.password.data:
            flash("Incorrect password")
            return redirect("/")

        session["user_id"] = old_user.user_id
        return redirect("/userprofile")
        flash("logged in")


@app.route('/', methods=['POST'])
def user_signup():
    """user signup"""

    form = UserForm(request.form)
    new_user = User(phone_number=form.phonenumber.data,
                    password=form.password.data)
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.user_id
    flash("user has been registered")
    return redirect("/preference")


@app.route("/preference", methods=['GET', 'POST'])
def preference():
    """getting user info from user"""
    if request.method == 'GET':
        # display form
        form = PreferenceForm()

        return render_template("Preference.html", form=form)

    else:
        # save prefdata
        user = User.query.get(session["user_id"])
        form = PreferenceForm(request.form)
        # get the user

        user.location = form.location.data


        db.session.add(user)
        db.session.commit()

        flash("preferences added to data base")
        return redirect("/userprofile")


@app.route("/userprofile")
def user_profile():
    """displaying user profile"""
    user = User.query.get(session["user_id"])

    return render_template("userprofile.html", 
        user_phonenumber=user.phone_number, 
        user_location=user.location)

# @app.route("/displaytrail")


def get_trails_from_location(location_of_trails):

    key = os.environ["YELP_API_KEY"]

    headers = {"Authorization": 'Bearer ' + key}
    payload = {"term": "hiking trails", "location": location_of_trails}
    r = requests.get("https://api.yelp.com/v3/businesses/search",
                     headers=headers, params=payload)
    hiking_trails = r.json()

    return hiking_trails["businesses"]


def filter_trails_by_rating(trails, rating=4):
    """filter trails by ratings"""
    filtered_trails = []
    for trail in trails:
        print(trail)
        if trail["rating"] >= rating:
            filtered_trails.append(trail)

    return filtered_trails


def get_random_trail(trails):
    """selecting random trail from best rating"""
    return random.choice(trails)

def make_directions_url(trail_address):
    """trail location coverted to google address"""

    base_url = 'https://www.google.com/maps/dir//'
    google_address = urllib.parse.quote_plus("\n".join(trail_address))
    return f"{base_url}{google_address}"


def trail_to_text_msg(trail):
    """message containing trail info"""
    trail_name = trail["name"]
    rating = trail["rating"]
    address = "\n".join(trail["location"]["display_address"])
    google_url = make_directions_url(address)

    return f"Trail name: {trail_name}\nRating: {rating}\nTrail location: {address}\nGet Directions: {google_url}"


@app.route("/send_msg")
def send_msg():
    """sending msg to user"""
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

        trails = get_trails_from_location(user_location)
        high_rating_trails = filter_trails_by_rating(trails)
        recommended_trail = get_random_trail(high_rating_trails)


        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body=f"Hi, here is our recommendation of a Hike trail for your weekend\n{trail_to_text_msg(recommended_trail)}",
                from_='+13347317307',
                to=user_phonenumber,
            )

    return message



@app.route("/send_msg_now")
def send_msg_now():
    """sending msg to the user in session if selected recoomend now"""
    account_sid = os.environ["account_sid"]
    auth_token = os.environ["auth_token"]
    user = User.query.get(session["user_id"])

    user_phonenumber = user.phone_number
    user_location = user.location


    trails = get_trails_from_location(user_location)


    high_rating_trails = filter_trails_by_rating(trails)

    recommended_trail = get_random_trail(high_rating_trails)

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f"Hi, here is our recommendation of a Hike trail for your weekend\n{trail_to_text_msg(recommended_trail)}",
            from_='+13347317307',
            to=user_phonenumber,
        )
    return "hike trail recommendation has been sent"


@app.route("/show_all_trails")
def show_all_trails():
    """Display all the trails of a specific location to user"""
    key = os.environ["YELP_API_KEY"]
    user = User.query.get(session["user_id"])
    user_location = user.location

    headers = {"Authorization": 'Bearer ' + key}
    payload = {"term": "hiking trails", "location": user_location}
    r = requests.get("https://api.yelp.com/v3/businesses/search",
                     headers=headers, params=payload)
    hiking_trails = r.json()
    list_trails_info = hiking_trails["businesses"]

    for trail in list_trails_info:
        display_address = trail["location"]["display_address"]
        # address = "\n".join(display_address)
        google_url = make_directions_url(display_address)
        trail["google_directions_address"] = google_url

    

    map_api = "https://maps.googleapis.com/maps/api/js?key={}&callback=myMap".format(map_key)

    return render_template("showalltrails.html", list_trails_info=list_trails_info, map_api=map_api)





@app.route('/logout')
def logout():
    """logout user"""
    del session["user_id"]
    flash("logged out")
    return redirect("/")


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0", port=6001)
