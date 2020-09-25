from flask import Flask, request
from flask_marshmallow import Marshmallow

from .models import Podcast

app = Flask(__name__)
ma = Marshmallow(app)


class PodcastSchema(ma.Schema):
    class Meta:
        model = Podcast
        fields = ('id', 'artist_name', 'release_date', 'name', 'copyright', 'url')