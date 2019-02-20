"""API requests and routes"""

from flask import Flask, request, redirect, render_template, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import requests

import spotifyutils
from settings import *
from model import db, connect_to_db, User, Activity, Playlist, Song, Playlist_Song 

app = Flask(__name__)
app.jinja_env.undefinded = StrictUndefined
app.debug = True

@app.route('/')
def index():
    """ Homepage """

    return render_template('homepage.html')

@app.route('/spotify-login')
def spotify_login():
    """ Spotify Authorization Page """

    spotify_auth_url = spotifyutils.generate_auth_url()

    return redirect(spotify_auth_url)

@app.route('/spotify-callback')
def spotify_callback():

    response_data = spotifyutils.get_access_token()
  
    session['spotify_token'] = response_data.get('access_token')

    return render_template('callback-page.html')

@app.route('/register-new-user', methods=['GET'])
def register_new_user():

    return render_template('register-new-user.html')

@app.route('/sign-up-verification', methods=["POST"])
def register_process():
    """ Register New User """

    username = request.form["new-username"]
    password = request.form["new-password"]

    user = User.query.filter(User.username==username).first()

    if user:
        flash("That username is already taken!")
        return redirect("/register-new-user")
    else:
        new_user = User(username=username, password=password)
        
        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.user_id
        session['logged_user'] = {  'user_id': user_id,
                                    'username': username,
                                    'password': password}

        flash(f"User {username} added.")

        return redirect("/activity-page")

@app.route('/login-current-user', methods=['GET'])
def login_form():

    return render_template("login-page.html")

@app.route('/login-verification', methods=["POST"])
def login_current_user():
    """ Login for Exisiting User """

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter(User.username==username).first()

    if user:
        if user.password == password:
            user_id = user.user_id
            session['logged_user'] = {  'user_id': user_id,
                                        'username': username}

            flash("You've successfully logged in!")
            return redirect("/activity-page")
        else:
            flash("The password is incorrect.")
    else:
        flash("That username doesn't exist!")
        return redirect("/login-current-user")

@app.route('/activity-page')
def display_activity():
    """ Activity Page """

    token = session['spotify_token']

    # print(spotifyutils.search_playlists())
    # print(spotifyutils.search_playlist_tracks())

    return render_template('activity-page.html')

@app.route('/logout')
def logout():
    """Log out"""

    del session["logged_user"]
    del session['spotify_token']
    flash("Logged Out.")

    return redirect("/")

'''
import pdb; pdb.set_trace()

'''





