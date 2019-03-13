from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trail, Favorites
from flask_wtf import FlaskForm
import requests
from wtforms import StringField, SelectField, SubmitField, BooleanField, PasswordField, validators, Form
import os
import random
from twilio.rest import Client
import urllib.parse
import bcrypt


class LocationChangeForm(FlaskForm):
    location = StringField('location', render_kw = {'placeholder': 'Enter your location'})
    submit = SubmitField("Edit Location!")

class SignupForm(FlaskForm):
    phonenumber = StringField('phone number', render_kw = {'class': 'logininput', 'placeholder': 'Enter your phone number for eg +14156905074'})
    password = PasswordField('password', render_kw = {'class': 'logininput', 'placeholder': 'Password'})
    location = StringField('location', render_kw = {'placeholder': 'Enter your location'})
    

    submit = SubmitField("Signup!")


class LogInForm(FlaskForm):
    phonenumber = StringField('phone number', render_kw = {'class': 'logininput', 'placeholder': 'Enter your phone number for eg +14156905074'})
    password = PasswordField('password', render_kw = {'class': 'logininput', 'placeholder': 'Password'})
    submit = SubmitField("SignIn")


app = Flask(__name__)


app.secret_key = os.environ["secret_key"]
map_key = os.environ["google_map_key"]
app.jinja_env.undefined = StrictUndefined




@app.route('/', methods=['GET', 'POST'])
def user_login():
    """user login"""
    if request.method == 'GET':

        form = LogInForm(request.form)

        return render_template("homepage.html", form=form)
    else:
        form = LogInForm(request.form)

        old_user = User.query.filter_by(
            phone_number=form.phonenumber.data).first()
        form_password = form.password.data
        if not old_user:
            flash("No such user")
            return redirect("/")

        # if bcrypt.checkpw(form_password.encode('utf-8'), old_user.password.encode('utf-8')):
        # if old_user.password != form.password.data:

            flash("Incorrect password")
            return redirect("/")
        if bcrypt.checkpw(form_password.encode('utf-8'), old_user.password.encode('utf-8')):
            session["user_id"] = old_user.user_id
            return redirect("/userprofile")
            flash("logged in")
        else:    
            flash("Incorrect password")
            return redirect("/")

@app.route('/logout')
def logout():
    """logout user"""
    del session["user_id"]
    flash("logged out")
    return redirect("/")        


@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    """user signup"""
    if request.method == 'GET':
        form = SignupForm(request.form)
        return render_template("signup.html", form=form)

    form = SignupForm(request.form)
    location = form.location.data
    password=form.password.data
    # new_user = User(phone_number=form.phonenumber.data,
    #                 password=form.password.data)
    hashed = str(bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt()), 'utf-8')
    users = User.query.filter_by(phone_number=form.phonenumber.data).all()
    if users:
        flash("user already exists")
        return redirect("/")
    new_user = User(phone_number=form.phonenumber.data,
                    password=hashed, location=form.location.data)
    

    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.user_id
    flash("user has been registered")
    return redirect("/userprofile")


@app.route("/editlocation", methods=['GET', 'POST'])
def editlocation():
    """getting user info from user"""
    if request.method == 'GET':
        # display form
        form = LocationChangeForm()

        return render_template("editlocation.html", form=form)

    else:
        # save prefdata
        user = User.query.get(session["user_id"])
        form = LocationChangeForm(request.form)
        # get the user

        user.location = form.location.data


        db.session.add(user)
        db.session.commit()
 
        flash("location changed")
        return redirect("/userprofile")



@app.route("/userprofile")
def user_profile():
    """displaying user profile"""
    user_id = session["user_id"]

    # user = User.query.get(session["user_id"])
    user = User.query.get(user_id)


    return render_template("userprofile.html", 
        user_phonenumber=user.phone_number, 
        user_location=user.location, 
        user=user)




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
    return redirect("/userprofile")


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

    user_trails = user.trails
    user_trails_name = [t.trail_name for t in user_trails]
    

    for trail in list_trails_info:
        display_address = trail["location"]["display_address"]
        # address = "\n".join(display_address)
        google_url = make_directions_url(display_address)
        trail["google_directions_address"] = google_url
        if trail["name"] in user_trails_name:
            trail["is_fav"] = True
        else:
            trail["is_fav"] = False



    

    map_api = "https://maps.googleapis.com/maps/api/js?key={}&callback=myMap".format(map_key)

    return render_template("showalltrails.html", list_trails_info=list_trails_info, map_api=map_api)

@app.route("/save-trails", methods=["POST"])
def save_fav_trails():
    img = request.form.get("trailImage")
    trailDir = request.form.get("trailDirections")
    trailUrl = request.form.get("trailUrl")
    trailName = request.form.get("trailName")


    trail = Trail(trail_name=trailName, trail_image=img,
            trail_google_direction=trailDir, trail_yelp_link=trailUrl)
    
    db.session.add(trail)
    db.session.commit()

    fav = Favorites(user_id=session["user_id"], trail_id=trail.trail_id)
    db.session.add(fav)
    db.session.commit()



    return "1"

@app.route("/unfav-trails", methods=["POST"])
def del_fav_trails():
    img = request.form.get("trailImage")
    trailDir = request.form.get("trailDirections")
    trailUrl = request.form.get("trailUrl")
    trailName = request.form.get("trailName")

    trail = Trail.query.filter_by(trail_name=trailName).first()
    fav = Favorites.query.filter_by(user_id=session["user_id"], trail_id=trail.trail_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
    return "1"






if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host="0.0.0.0", port=6001)
