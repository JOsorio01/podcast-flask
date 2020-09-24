from flask import Flask, request
from flask_restful import Api, Resource
from resources.podcast import PodcastViews
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = SQLAlchemy(app)

podcast_genres = db.Table('podcast_genre',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True),
    db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id'), primary_key=True)
)

class Genre(db.Model):
    id = db.Column('genre_id', db.Integer(), primary_key=True)
    name = db.Column('name', db.String(250))
    url = db.Column('url', db.Text())


class Podcast(db.Model):
    """Model for podcast, removed some non common fields (for test purposes)"""
    id = db.Column('id', db.Integer(), primary_key=True)
    artist_name = db.Column('artist_name', db.String(250))
    release_date = db.Column('release_date', db.Date())
    name = db.Column('name', db.String(250))
    copyright = db.Column('copyright', db.Text())
    url = db.Column('url', db.Text())

    def __init__(self, id, artist_name, release_date, name, copyright, url):
        self.id = id
        self.artist_name = artist_name
        self.release_date = release_date
        self.name = name
        self.copyright = copyright
        self.url = url    

# db.create_all()

podcast = PodcastViews()

class FromSourcePodcastView(Resource):
    def get(self, podcast_id=None):
        if podcast_id: 
            return podcast.get_podcast(podcast_id)
        return podcast.get_podcasts(request)

    def delete(self, podcast_id=None):
        if podcast_id: 
            return podcast.delete_podcast(podcast_id)
        return "Podcast ID was not providen", 403

class FromSourceFirst20Records(Resource):
    def get(self):
        return podcast.first_20_podcast(request)

class FromSourceLast20Records(Resource):
    def get(self):
        return podcast.last_20_podcast(request)

api.add_resource(FromSourcePodcastView, '/from_source/', '/from_source/<int:podcast_id>')
api.add_resource(FromSourceFirst20Records, '/from_source/first20', '/from_source/first20.json')
api.add_resource(FromSourceLast20Records, '/from_source/last20', '/from_source/last20.json')

@app.route('/create-records')
def create_records():
    for p in podcast.podcast_list:
        db.session.add(
            Podcast(
                id=p.get('id', None),
                artist_name=p.get('artistName', None),
                release_date=datetime.strptime(p.get('releaseDate', ''), "%Y-%m-%d"),
                name=p.get('name', None),
                copyright=p.get('copyright', ''),
                url=p.get('url', '')
            )
        )
        db.session.commit()
    return {"msg": "created"}
        
@app.route('/')
def test():
    p = Podcast.query.all()
    print(len(p))
    return {"msg": "asdasd"}


if __name__ == '__main__':
    app.run(debug=True)
