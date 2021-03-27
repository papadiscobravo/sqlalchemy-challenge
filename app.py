# This is app.py for my HW10 assignment: SQLAlchemy Challenge.
# starter files:
# hawaii.sqlite
# SQLAlchemyChallenge.ipynb


# 1 Import Flask...
from flask import Flask, jsonify

# ... et al.
import datetime as dt
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
    print(f"Server received request for HW10-Hawaii weather home page...")
    return "Welcome to the HW10-Hawaii weather home page. Your routes are:<br>\
    <a href='/api/v1.0/precip'>/api/v1.0/precip</a><br>\
    <a href='/api/v1.0/stations'>/api/v1.0/stations</a><br>\
    <a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br>\
    <a href='/api/v1.0/<start>/<end>'>/api/v1.0/<start>/<end></a><br>\
    <a href='/api/v1.0/contact'>/api/v1.0/contact</a><br>"


# /api/v1.0/precip

# a Convert the query results to a dictionary using date as the key and prcp as the value.
# b Return the JSON representation of your ditionary.

@app.route("/api/v1.0/precip")
# print(f"Server received request for station data...")
# Create session (link) from Python to the database: 
def precip():
    session = Session(engine)
# Query the database:
    results = session.query(Measurement.date, Measurement.prcp).all()
# Don't forget to close the session or there will be an orphaned session
# lurking around causing things to behave erratically:
    session.close()
    all_measurements = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_measurements.append(prcp_dict)
    return jsonify(all_measurements)


# /api/v1.0/stations
# weather_stations = {"name": [], "id": [], "elevation": [], "latitude": [], "station": [], "longitude": []}

# Return a JSON list of stations from the dataset.
# (There must be a query to populate weather_stations.)

@app.route("/api/v1.0/stations")
def stations():
# print(f"Server received request for station data...")
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    weather_stations = list(np.ravel(results))
#    return f"Here are the Hawaii weather station in the data.<br>\
#    <a href='/'>home</a>br\
#    {jsonify(weather_stations)}"
    return jsonify(weather_stations)

# /api/v1.0/tobs

# a Query the dates and temperature observations of the most active station for the last year of data.
# b Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
# Calculate the start of the most recent year in the weather measurements
    most_recent_yr_start = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Find the most active station:
#   create session (link) from Python to the database: 
    session = Session(engine)
#   query
    result = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active_station = result[0][0]

    print(f"Server received request for temperature observations (TOBS) from the previous year at {most_active_station}...")
#   (Terminal should indicate station USC00519281 has been found.)

# Query the database for TOBS from {most_recent_yr_start} at {most_active_station}:
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= most_recent_yr_start).all()

# Close the session:
    session.close()

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)


    return jsonify(all_tobs)

# If {results} is a list of tuples, convert it into a normal list:
#    tobs = list(np.ravel(results))
# return jsonify(tobs)


# /api/v1.0/<start>
# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
# print(f"Server received request for weather data {start} through {end}...")
    # return "Here's some Hawaii weather data {start} through {end}.<br>\
    # <a href='/'>home</a>"
    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        return jsonify(results)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    return jsonify(results)

    session.close()


# /api/v1.0/contact
@app.route("/api/v1.0/contact")
def contact():
# print(f"Server received request for contact info...")
    email = "papadiscobravo@gmail.com"
    return f"Email {email} with questions.<br><a href='/'>home</a>"

# 4 Define main behavior.
#
# LOOK      LOOK      LOOK      LOOK      LOOK      LOOK      LOOK     
# Code has to have this at the end or something/everything will blow up:
#      LOOK      LOOK      LOOK      LOOK      LOOK      LOOK      LOOK
#
if __name__ == '__main__':
    app.run(debug=True)