from flask import Flask, request
from flask_restful import Api, Resource
from podcast.views import get_podcasts, first_20_podcast, last_20_podcast

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return get_podcasts(request)

class First20Records(Resource):
    def get(self):
        return first_20_podcast(request)

class Last20Records(Resource):
    def get(self):
        return last_20_podcast(request)

api.add_resource(Home, '/')
api.add_resource(First20Records, '/first20', '/first20.json')
api.add_resource(Last20Records, '/last20', '/last20.json')

if __name__ == '__main__':
    app.run(debug=True)
