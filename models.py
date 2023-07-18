from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Retrieving data from .env file
import os
from dotenv import load_dotenv

load_dotenv()
# Assigning variables from .env file
db_URI = os.getenv("URI")

db = SQLAlchemy()
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = db_URI
# db.init_app(app)


# Our models


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.String(100), nullable=False)

    user_beats = db.relationship("Beats", backref="user")
    user_tracks = db.relationship("Tracks", backref="user")


class Beats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(100), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sc_id = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    fk_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(100), nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sc_id = db.Column(db.String(255), nullable=False)
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    beat_id = db.Column(db.Integer, db.ForeignKey("beats.id"), nullable=False)
