from flask import Response

import requests as rq
import json

SOURCE_URL = "https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json"


class PodcastViews:
    def __init__(self):
        self.podcast_list = self.get_podcast_data()

    @staticmethod
    def get_podcast_data():
        # Read data for manipulation
        data = rq.get(SOURCE_URL).json()
        # Data loaded from a file would have the same treatment
        # with open('data.json') as json_file:
        #     data = json.load(json_file)
        return data['feed']['results']  # This is all important data

    def get_podcast(self, podcast_id):
        podcast = list(filter(
            lambda val: str(podcast_id) in val['id'],
            self.podcast_list
        ))
        if podcast:
            return podcast[0]
        return {"message": "Podcast not found"}, 404

    def get_podcasts(self, request):
        """Read podcast data from url and retrieve"""
        name = request.args.get('name', '')
        artist = request.args.get('artist', '')
        # Filter results data and replace
        return list(filter(
            lambda val:
                name.lower() in val['name'].lower()
                and artist.lower() in val["artistName"].lower(),
            self.podcast_list
        ))

    @staticmethod
    def response_to_json_file(data):
        response = Response(content_type='application/json')
        response.data = json.dumps(data)
        response.headers['Content-Disposition'] = 'attachment; filename="%s"' % 'top20podcast.json'
        return response

    def first_20_podcast(self, request):
        """Return top 20 podcast"""
        if '.json' in request.path:
            return self.response_to_json_file(self.podcast_list[0:20])
        return self.podcast_list[0:20]

    def last_20_podcast(self, request):
        """Return bottom 20 podcast"""
        data = self.podcast_list
        data.reverse()
        data = data[0:20]
        if '.json' in request.path:
            return self.response_to_json_file(data)
        return data

    def delete_podcast(self, podcast_id):
        obj = list(filter(
            lambda val: str(podcast_id) in val['id'],
            self.podcast_list
        ))
        if obj:
            del self.podcast_list[self.podcast_list.index(obj[0])]
            return {"message": "Podcast was deleted"}, 200
        return {"message": "Podcast not found"}, 404
