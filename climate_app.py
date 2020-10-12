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

@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the query results to a dictionary using date as the key and prcp as the value    
        print("Server received request for 'precipitation' page...")
        # Calculate the Date 1 Year Ago from the Last Data Point in the Database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        
        prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
        
        # Convert List of Tuples Into a Dictionary
        prcp_data_list = dict(prcp_data)
        
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)

# This final if statement simply allows us to run in "Development" mode, which 
# means that we can make changes to our files and then save them to see the results of 
# the change without restarting the server.

if __name__ == "__main__":
    app.run(debug=True)