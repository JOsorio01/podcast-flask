from flask import request
from flask_restful import Resource
from sqlalchemy import or_

from .schemas import PodcastSchema
from .models import Podcast, delete
from .podcast import PodcastSource


class PodcastView(Resource):

    def get(self, pk=None):
        if pk:
            results = Podcast.query.get(pk)
            podcast_schema = PodcastSchema()
            return podcast_schema.jsonify(results)
        else:
            search = request.args.get('search', '')
            results = Podcast.query.filter(or_(
                Podcast.name.like('%{0}%'.format(search)),
                Podcast.artist_name.like('%{0}%'.format(search))
            ))
            schema = PodcastSchema(many=True)
            return schema.jsonify(results)

    def delete(self, pk):
        if pk:
            try:
                delete(Podcast.query.get(pk))
            except Exception as msg:
                print(msg)
                return {"message": "Cannot delete recort"}, 404
            return {"message": "Record was deleted"}, 200
        return {"message": "Podcast id was not providen"}, 403

class Top20PodcastView(Resource):
    def get(self):
        results = Podcast.query.all()[0:20]
        schema = PodcastSchema(many=True)
        if '.json' in request.path:
            return PodcastSource.response_to_json_file(schema.dump(results))
        return schema.jsonify(results)

class Last20PodcastView(Resource):
    def get(self):
        results = Podcast.query.all()
        results.reverse()
        results = results[0:20]
        schema = PodcastSchema(many=True)
        if '.json' in request.path:
            return PodcastSource.response_to_json_file(schema.dump(results))
        return schema.jsonify(results)