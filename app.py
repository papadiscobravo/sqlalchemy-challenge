# This is app.py for my HW10 assignment: SQLAlchemy Challenge.
# starter files:
# hawaii.sqlite
# SQLAlchemyChallenge.ipynb


# 1 Import Flask...
from flask import Flask, jsonify

# ... et al.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# 2 Set up Flask / create an app
app = Flask(__name__)   


# 2.1 do database setup

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# hawaii.sqlite has two tables:
# Station
# Measurement
# I worked with them in Jupyter Notebook.
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


# 3. Define routes

# list routes
# /
#   Home page.
#   List all routes that are available.
#   the four routes:
#      precip
#      stations
#      tobs
#      start and end

@app.route("/")
def home():
#    print(f"Server received request for HW10-Hawaii weather home page...")
    return "Welcome to the HW10-Hawaii weather home page. Your routes are:<br>\
    <a href='/api/v1.0/precip'>/api/v1.0/precip</a><br>\
    <a href='/api/v1.0/stations'>/api/v1.0/stations</a><br>\
    <a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br>\
    <a href='/api/v1.0/<start_date>'>/api/v1.0/<start_date></a><br>\
    <a href='/api/v1.0/contact'>/api/v1.0/contact</a><br>"


# /api/v1.0/precip

# a Convert the query results to a dictionary using date as the key and prcp as the value.
# b Return the JSON representation of your ditionary.

@app.route("/api/v1.0/precip")
def precip():
#    print(f"Server received request for station data...")
# Create session (link) from Python to the database: 
    session = Session(engine)

# Query the database:
    results = session.query(Measurement.date, Measurement.prcp).all()

# Don't forget to close the session or there will be an orphaned session
# lurking around the Flask server trying up system resources and if that
# happens enough times it will affect server performance and perhaps even
# make the server behave more unhappily than that:
    session.close()

# Can try returning {results} jsonified...
#    return jsonify(results)

# ...or, if {results} is a list of tuples, convert it into a normal list:
    all_measurements = list(np.ravel(results))
    return jsonify(all_measurements)


# /api/v1.0/stations

# weather_stations = {"name": [], "id": [], "elevation": [], "latitude": [], "station": [], "longitude": []}

# Return a JSON list of stations from the dataset.
# (There must be a query to populate weather_stations.)

@app.route("/api/v1.0/stations")
def stations():
#    print(f"Server received request for station data...")
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    weather_stations = list(np.ravel(results))
#    return f"Here are the Hawaii weather station in the data.<br>\
#    <a href='/'>home</a>br\
#    {jsonify(weather_stations)}"
    return jsonify(weather_stations)

# /api/v1.0/tobs

tobs = {"date": [], "station": [], "tobs": []}

# a Query the dates and temperature observations of the most active station for the last year of data.
# b Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
 #   print(f"Server received request for tobs...")
    return "fHere's some Hawaii tobs data.<br>\
    <a href='/'>home</a><br>\
    {jsonify(tobs)}"
    return jsonify(tobs)

# /api/v1.0/<start_date>

# start_date = "2011-01-01"

@app.route("/api/v1.0/<start_date>")
def start():
#    print(f"Server received request for weather data starting {start_date}...")
    return "Here's some Hawaii weather data starting {start_date}.<br>\
    <a href='/'>home</a>"

# /api/v1.0/contact
@app.route("/api/v1.0/contact")
def contact():
    email = "papadiscobravo@gmail.com"
#    print(f"Server received request for contact info...")
    return f"Email {email} with questions.<br><a href='/'>home</a>"

# 4 Define main behavior.
#
# LOOK      LOOK      LOOK      LOOK      LOOK      LOOK      LOOK     
#      LOOK      LOOK      LOOK      LOOK      LOOK      LOOK      LOOK
# Code has to have this at the end or something/everything will blow up:
#
if __name__ == '__main__':
    app.run(debug=True)