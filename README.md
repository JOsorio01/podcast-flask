# podcast-flask

Source data: https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/100/explicit.json
## Solution
* Using Jupyter Notebook to fetch data from the source URL to read the json and handle data and know the labels, where I found the main data where under the label of ‘results’ inside the ‘feed’ the principal label.
* After knowing the data to work with, I started a Flask Restful project to make the API. Started building endpoints fetching the url data to pre-process and send the required responses.
* For store all data in a sqlite3 database I made a script to fetch the source data and for each podcast and genre create a new record in database also respecting the primary keys constraints.
* Also I tried to make a well-structured project
## Installation

### Requirements:
* Python 3.7 or higher.
* Python or Anaconda virtual environment with pip
* Clone the project and with an active virtual environment enter the main folder and there is a ‘requirements.txt’ file, then run:
		`$ pip install -r requirements.txt`
	It will all the dependencies for the project
  
* __The project structure__:
```
podcast-flask/
+-- resources/
|  +-- __init__.py
|  +-- models.py (model classes)
|  +-- podcast.py (views that use data directly from the source using requests library)
|  +-- schemas.py (Schema classes for model objects serialization)
|  +-- utils.py
|  +-- views.py (view classes that use data from the sqlite database)
+-- .gitignore
+-- app.py (where app runs also routes and flask configurations)
+-- data.json (json file with data from the source - used for making the podcast views using json file instead of fetching data)
+-- database.sqlite (built-in database)
+-- fill_database.py (python script that cleans and generates all data for the sqlite database using the source data)
+-- README.md
+-- requirements.txt (all project dependencies)
```
* Prepare database using the following commands on the project directory:
```
python resources/models.py db init
python resources/models.py db migrate
python resources/models.py db upgrade
python fill_database.py
```
* In terminal inside the project directory run:
          `$ python app.py`
	This will run the debug server on (http://127.0.0.1:5000)
  
## Endpoints

### GET

  `http GET http://127.0.0.1:5000`

  `http GET http://127.0.0.1:5000?search={search} -> filter matching artist or name`
  
  `http GET http://127.0.0.1:5000/{id}`
  
  `http GET http://127.0.0.1:5000/genre`
  
  `http GET http://127.0.0.1:5000/genre/{id}`
  
  `http GET http://127.0.0.1:5000/top20`
  
  `http GET http://127.0.0.1:5000/top20.json`
  
  `http GET http://127.0.0.1:5000/last20`
  
  `http GET http://127.0.0.1:5000/last20.json`
  
  `http GET http://127.0.0.1:5000/from_source`

  `http GET http://127.0.0.1:5000/from_source?artist={artist}&name={name} -> filter matching artist or name`
  
  `http GET http://127.0.0.1:5000/from_source/{id}`
  
  `http GET http://127.0.0.1:5000/from_source/first20`
  
  `http GET http://127.0.0.1:5000/from_source/first20.json`
  
  `http GET http://127.0.0.1:5000/from_source/last20`
  
  `http GET http://127.0.0.1:5000/from_source/last20.json`
  
### DELETE
  `http DELETE http://127.0.0.1:5000/{id}`
