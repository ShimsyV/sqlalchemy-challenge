# import Flask
from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)

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

# This final if statement simply allows us to run in "Development" mode, which 
# means that we can make changes to our files and then save them to see the results of 
# the change without restarting the server.

if __name__ == "__main__":
    app.run(debug=True)