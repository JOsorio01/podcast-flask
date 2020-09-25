from werkzeug.security import generate_password_hash
from resources.models import db, Podcast, Genre, User
from resources.podcast import PodcastSource

from datetime import datetime
import uuid

# Reload tables
db.drop_all()
db.create_all()

podcast_list = PodcastSource.get_podcast_data()

# Create one user for authentication matters
hashed_pwd = generate_password_hash('secret123!')
user = User(user_uuid=str(uuid.uuid4()), username='user', password=hashed_pwd)
db.session.add(user)
print("User created {0}".format(user))

# Create podcast and genres
for p in podcast_list:
    podcast = Podcast(
        id=p.get('id', ''),
        artist_name=p.get('artistName', ''),
        release_date=datetime.strptime(p.get('releaseDate', ''), "%Y-%m-%d"),
        name=p.get('name', ''),
        copyright=p.get('copyright', ''),
        url=p.get('url', '')
    )
    db.session.add(podcast)
    for g in p['genres']:
        genre = Genre.query.get(g['genreId'])
        if not genre:
            genre = Genre(
                id=g.get('genreId', ''),
                name=g.get('name', ''),
                url=g.get('url', '')
            )
        db.session.add(genre)
        podcast.genres.append(genre)

db.session.commit()
print("Created podcast and genres")
