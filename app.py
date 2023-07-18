from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import bcrypt
import psycopg2

from models import db, Users, Beats, Tracks

# Retrieving data from .env file
import os
from dotenv import load_dotenv

load_dotenv()

# Assigning variables from .env file
db_URI = os.getenv("URI")
secret_key = os.getenv("secret_key")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_URI
app.config["SECRET_KEY"] = secret_key
# db = SQLAlchemy()
db.init_app(app)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

with app.app_context():
    db.create_all()


@app.route("/")
def base():
    return render_template("base.html")


@app.route("/users")
def user_list():
    users = db.session.execute(
        db.select(Users.id, Users.username, Users.email, Users.pw_hash).order_by(
            Users.id
        )
    ).fetchall()
    return render_template("user/list.html", users=users)


@app.route("/users/create", methods=["POST"])
def user_create():
    user_password = request.form["password"].encode()

    password_hash = bcrypt.hashpw(user_password, bcrypt.gensalt()).decode()

    user = Users(
        account_type=request.form["account_type"],
        username=request.form["username"],
        email=request.form["email"],
        pw_hash=password_hash,
    )
    db.session.add(user)
    db.session.commit()
    # name = db.session.execute(db.select)
    # session["user_name"] = name[0]
    return redirect(url_for("base", id=user.id))


@app.route("/users/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password").encode()

    user = Users.query.filter_by(email=email).first()

    if user == None:
        pass
    else:
        pw_hash = user.pw_hash.encode()
        result = bcrypt.checkpw(password, pw_hash)
        if result == False:
            pass
        else:
            name = user.username
            id = user.id
            session["user_name"] = name
            session["user_id"] = id
            return redirect(url_for("base"))


@app.route("/users/logout")
def logout():
    session.clear()
    return redirect(url_for("base"))


@app.route("/upload_beat/<id>", methods=["POST"])
def upload_beat(id):
    sc__embed_link = request.form.get("sc_embed")
    index_start = sc__embed_link.find("tracks/") + 7
    index_end = sc__embed_link.find("&color")
    sc_code = sc__embed_link[slice(index_start, index_end)]

    beat = Beats(
        track_name=request.form["name"],
        sc_id=sc_code,
        fk_user_id=id,
    )
    db.session.add(beat)
    db.session.commit()
    return redirect(url_for("base"))


@app.route("/upload_rap/<id>/<beat_id>", methods=["POST"])
def upload_rap(id, beat_id):
    sc__embed_link = request.form.get("sc_embed")
    index_start = sc__embed_link.find("tracks/") + 7
    index_end = sc__embed_link.find("&color")
    sc_code = sc__embed_link[slice(index_start, index_end)]

    track = Tracks(
        track_name=request.form["name"],
        sc_id=sc_code,
        user_id=id,
        beat_id=beat_id,
    )
    db.session.add(track)
    db.session.commit()

    return redirect(url_for("show_track", track_id=beat_id))


@app.route("/users/profile/<id>", methods=["GET"])
def show_profile(id):
    user = db.get_or_404(Users, id)

    if user.account_type == "producer":
        beats = Beats.query.filter_by(fk_user_id=id)
        print(beats)

        user_name = user.username
        account_type = user.account_type
        user_id = user.id
        return render_template(
            "/user/profile.html",
            account_type=account_type,
            user_id=user_id,
            user_name=user_name,
            beats=beats,
        )


@app.route("/tracks/<track_id>")
def show_track(track_id):
    track = db.get_or_404(Beats, track_id)
    sc_id = track.sc_id
    return render_template("/tracks.html", sc_id=sc_id, track_id=track_id)


@app.route("/browse")
def browse():
    music = db.session.query(Beats).all()
    print(music)
    return render_template("/browse.html", music=music)


# @app.route("/")
# def index():
#     # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
#     # Connection info below is for the RENDER.COM database connection, switch on when pushing to github...but hang on, it's not for SQL Alchemy.... :/
#     # connection = psycopg2.connect(os.getenv("DATABASE_URL"))
#     # cursor = connection.cursor()
#     # cursor.execute("SELECT * FROM users;")
#     results = cursor.fetchall()
#     # connection.close()
#     return f"{results}"


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
