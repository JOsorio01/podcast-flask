from flask import Flask, request
from flask_restful import Api, Resource
from resources.podcast import Podcast

app = Flask(__name__)
api = Api(app)
podcast = Podcast()


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

if __name__ == '__main__':
    app.run(debug=True)
