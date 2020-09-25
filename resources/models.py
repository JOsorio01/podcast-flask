from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

# Settings
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

podcast_genres = db.Table('podcast_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True),
    db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id'), primary_key=True)
)


class Genre(db.Model):

    __tablename__ = 'genre'

    id = db.Column('genre_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    url = db.Column('url', db.Text)

    def __repr__(self):
        return '<Genre Table {0}>'.format(self.id)


class Podcast(db.Model):

    __tablename__ = 'podcast'

    id = db.Column('id', db.Integer, primary_key=True)
    artist_name = db.Column('artist_name', db.String(250))
    release_date = db.Column('release_date', db.Date)
    name = db.Column('name', db.String(250))
    copyright = db.Column('copyright', db.Text)
    url = db.Column('url', db.Text)

    # Relationships
    genres = db.relationship(
        'Genre', secondary=podcast_genres, lazy='dynamic',
        backref=db.backref('podcast_genres', lazy=True)
    )

    def __repr__(self):
        return '<Podcast Table {0}>'.format(self.id)


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User Table {0}>'.format(self.username)


def delete(obj):
    db.session.delete(obj)
    db.session.commit()
