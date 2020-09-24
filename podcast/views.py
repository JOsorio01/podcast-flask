from flask import Response

import requests as rq
import json

SOURCE_URL = "https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json"

def get_podcast_data():
    # Read data for manipulation
    data = rq.get(SOURCE_URL).json()
    # Raw data contains one key -> 'feed'
    # Data whom will be sorted is in 'results' key
    return data['feed']['results']  # This is all important data

def get_podcasts(request):
    """Read podcast data from url and retrieve"""
    name = request.args.get('name', '')
    artist = request.args.get('artist', '')
    results = get_podcast_data()
    # Filter results data and replace
    return list(filter(
        lambda val:
            name.lower() in val['name'].lower()
            and artist.lower() in val["artistName"].lower(),
        results
    ))

def response_to_json_file(data):
    response = Response(content_type='application/json')
    response.data = json.dumps(data)
    response.headers['Content-Disposition'] = 'attachment; filename="%s"' % 'top20podcast.json'
    return response

def first_20_podcast(request):
    """Return top 20 podcast"""
    data = get_podcast_data()[0:20]
    if '.json' in request.path:
        return response_to_json_file(data)
    return data

def last_20_podcast(request):
    """Return bottom 20 podcast"""
    data = get_podcast_data()
    data.reverse()
    data = data[0:20]
    if '.json' in request.path:
        return response_to_json_file(data)
    return data
