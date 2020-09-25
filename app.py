from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from resources.podcast import PodcastSource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from resources.models import db, User
from resources.views import PodcastView, Top20PodcastView, Last20PodcastView, GenreView

import datetime
import jwt

app = Flask(__name__)
api = Api(app)
# Settings
app.config['SECRET_KEY'] = "my_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Routes
api.add_resource(PodcastView, '/', '/<int:pk>', methods=['GET', 'DELETE'])
api.add_resource(Top20PodcastView, '/top20', '/top20.json')
api.add_resource(Last20PodcastView, '/last20', '/last20.json')
api.add_resource(GenreView, '/genre', '/genre/<int:pk>')

# Auth routes
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}
        )
    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('User not found', 404)
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
                "user_uuid": user.user_uuid,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            }, app.config['SECRET_KEY'])
        return jsonify({"token": token.decode('UTF-8')})
    return make_response(
        'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}
    )

# Views that take data from the given url source
podcast = PodcastSource()


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
