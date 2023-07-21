from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import cloudinary, cloudinary.uploader, cloudinary.api
import bcrypt
import psycopg2

from models import db, Users, Beats, Raps

import os

config = cloudinary.config(secure=True)

db_URI = os.getenv("URI")
secret_key = os.getenv("secret_key")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_URI
app.config["SECRET_KEY"] = secret_key
db.init_app(app)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

with app.app_context():
    db.create_all()


@app.route("/")
def base():
    top_beat = Beats.query.order_by(Beats.likes.desc()).first()
    print(top_beat)
    top_rap = Raps.query.order_by(Raps.likes.desc()).first()
    print(top_rap)
    return render_template("base.html", top_beat=top_beat, top_rap=top_rap)


@app.route("/signup")
def signup():
    return render_template("signup.html")


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
        profile_pic=request.form["profile_picture"],
        username=request.form["username"],
        email=request.form["email"],
        pw_hash=password_hash,
    )
    db.session.add(user)
    db.session.commit()
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
            session["account_type"] = user.account_type
            return redirect(url_for("base"))


@app.route("/users/logout")
def logout():
    session.clear()
    return redirect(url_for("base"))


@app.route("/upload_beat/<id>", methods=["POST"])
def upload_beat(id):
    beat = Beats(
        track_name=request.form["name"],
        audio_url=request.form["audio_url"],
        artwork_url=request.form["artwork_url"],
        fk_user_id=id,
    )
    db.session.add(beat)
    db.session.commit()
    return redirect(url_for("base"))


@app.route("/upload_rap/<id>/<beat_id>", methods=["POST"])
def upload_rap(id, beat_id):
    rap = Raps(
        audio_url=request.form["audio_url"],
        user_id=id,
        beat_id=beat_id,
    )
    db.session.add(rap)
    db.session.commit()

    return redirect(url_for("show_track", track_id=beat_id))


@app.route("/users/profile/<id>", methods=["GET"])
def show_profile(id):
    user = db.get_or_404(Users, id)

    if user.account_type == "producer":
        beats = Beats.query.filter_by(fk_user_id=id)

        return render_template(
            "/user/profile_producer.html",
            user=user,
            beats=beats,
        )
    else:
        raps = Raps.query.filter_by(user_id=id)
        return render_template(
            "/user/profile_mc.html",
            user=user,
            raps=raps,
        )


@app.route("/tracks/<track_id>")
def show_track(track_id):
    page_track = db.get_or_404(Beats, track_id)
    raps = Raps.query.filter_by(beat_id=track_id)
    return render_template(
        "/tracks.html", page_track=page_track, track_id=track_id, raps=raps
    )


@app.route("/browse")
def browse():
    return render_template("/browse.html")


@app.route("/browse/beats")
def browse_beats():
    beats = db.session.query(Beats).all()
    return render_template("/browse/beats.html", musics=beats)


@app.route("/browse/raps")
def browse_raps():
    raps = db.session.query(Raps).all()
    return render_template("/browse/raps.html", musics=raps)


if __name__ == "__main__":
    app.run(debug=False, port=os.getenv("PORT", default=5000))
