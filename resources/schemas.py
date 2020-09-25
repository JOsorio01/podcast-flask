from flask import Flask, request
from flask_marshmallow import Marshmallow

from .models import Podcast, Genre

app = Flask(__name__)
ma = Marshmallow(app)


class PodcastSchema(ma.Schema):
    class Meta:
        model = Podcast
        fields = ('id', 'artist_name', 'release_date', 'name', 'copyright', 'url')


class GenreSchema(ma.Schema):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'url', 'podcast_genres')

    podcast_genres = ma.Nested(PodcastSchema, many=True)
