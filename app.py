# This is app.py for my HW10 assignment: SQLAlchemy Challenge.

# starter files:
# hawaii.sqlite
# SQLAlchemyChallenge.ipynb

# import numpy, sqlalchemy, and flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save reference to the table
Weather = Base.classes.measurement

# create an app
app = Flask(__name__)   

# list routes
# /
#   Home page.
@app.route("/")
def home():
    print("Server received request for HW10-Hawaii weather home page...")
    return "Welcome to the HW10-Hawaii weather home page."

@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page."

#
#
#
#   List all routes that are available.

# /api/v1.0/precipitation
weather_dict = {
    "date": [],
    "prcp": []
    }

@app.route("/normal")
def normal():
    return weather_dict

@app.route("/jsonified")
def jsonified():
    return jsonify(weather_dict)

#   Convert the query results to a dictionary using date as the key and prcp as the value.
#   Return the JSON representation of your dictionary.

@app.route("/api/v1.0/weather")
def weather():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    weather_results = session.query(weather_dict.name).all()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

    session.close()





# /api/v1.0/stations
#   Return a JSON list of stations from the dataset.

# /api/v1.0/tobs
#   Query the dates and temperature observations of the most active station for the last year of data.
#   Return a JSON list of temperature observations (TOBS) for the previous year.

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
#   Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#   When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# Hints
#   You will need to join the station and measurement tables for some of the queries.
#   Use Flask jsonify to convert your API data into a valid JSON response object.


#
#
#
#
#
#
#
# more code that might be helpful?
@app.route("/api/v1.0/justice-league")
def justice_league():
    """Return the justice league data as json"""

    return jsonify(justice_league_members)


@app.route("/api/v1.0/justice-league/<real_name>")
def justice_league_character(real_name):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = real_name.replace(" ", "").lower()
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404




@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
