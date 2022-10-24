from crypt import methods
from multiprocessing.sharedctypes import Value
from signal import alarm
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import youtube, spotify, helpers


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect("youtify.db", check_same_thread=False)
db = connection.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Index
@app.route("/")
@helpers.login_required
def index():
    return render_template("index.html")

@app.route("/transfer", methods=["GET", "POST"])
@helpers.login_required
def transfer():
    if request.method == "POST":
        playlist_input = request.form.get("playlist_url")
        playlist_name = request.form.get("pl_name")
        public = request.form.get("public")

        playlist_url = helpers.check_url(playlist_input)

        if playlist_url == 1:
            return render_template("error.html", value = "Invalid playlist URL")

        if not playlist_name:
            playlist_name = "New Playlist"

        if not public:
            public = False
        else:
            public = True

        # Transferring the playlist
        songs_info = youtube.initiate_youtube(playlist_url)
        playlist = spotify.create_playlist(name=playlist_name, public=public)
        playlist_id = spotify.get_playlist_id(playlist)
        spotify.add_song_to_playlist(playlist_id, songs_info)
        songs = youtube.length(songs_info)

        return render_template("success.html", songs = songs)

    return render_template("transfer.html")

# About page
@app.route("/about")
@helpers.login_required
def about():
    return render_template("about.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = (request.form.get("username"))

        password = (request.form.get("password"))

        if not username:
            return render_template("error.html", value = "missing username")

        if not request.form.get("password"):
            return render_template("error.html", value = "missing password")

        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = db.fetchall()

        if len(rows) != 1:
            return render_template("error.html", value="Invalid Username or password")
        else:
            if not check_password_hash(rows[0][2], password):
                return render_template("error.html", value="Invalid Username or password")

        session["user_id"] = rows[0]
        return redirect("/")

    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Register page
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")
        hash = generate_password_hash(request.form.get("password"))

        db.execute("SELECT username FROM users")
        rows_db = db.fetchall()
        rows = []
        for i in range(len(rows_db)):
            row = rows_db[i][0]
            rows.append(row)
        print(rows)

        if password != confirmation:
            return render_template("error.html", value="Confirmation password does not correspond to Password")

        if (username.lower() not in rows):
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash,))
            connection.commit()
            db.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = db.fetchall()

            session["user_id"] = user_id

            return redirect("/")

        else:
            return render_template("error.html", value="Username already exists")

    return render_template("register.html")

@app.route("/news")
@helpers.login_required
def news():
    return render_template("news.html")
