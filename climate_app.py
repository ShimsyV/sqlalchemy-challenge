# # Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the Tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to the Database
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define what to do when a user hits the index route

@app.route("/")
def home():
    """List all available api routes."""
    print("Server received request for 'Home' page...")
    return (
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- Dates and Precipitation observations from the last year<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- Temperature Observations from the past year<br/>"
        f"/api/v1.0/<start><br/>"
        f"- minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date.<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- Minimum temperature, the average temperature, and the max temperature for dates between the start and end date inclusive."
        )

# Precipitation route

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        print("Server received request for 'Precipitation' page...")
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
        # Convert List of Tuples into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)


# Stations route

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        print("Server received request for 'Stations' page...")
        # Return a JSON List of Stations from the Dataset
        stations_all = session.query(Station.station, Station.name).all()
        # Convert List of Tuples into a dictionary
        station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
        print("Server received request for 'tobs' page...")
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of temperature Data Selecting Only the `date` and `tobs` Values
        tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
        # Convert List of Tuples into dictionary
        tobs_data_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
    print("Server received request for 'start' page...")
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).group_by(Measurement.date).all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)



@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
    print("Server received request for 'start & End' page...")
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).group_by(Measurement.date).all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

# This final if statement simply allows us to run in "Development" mode, which 
# means that we can make changes to our files and then save them to see the results of 
# the change without restarting the server.

if __name__ == "__main__":
    app.run(debug=True)