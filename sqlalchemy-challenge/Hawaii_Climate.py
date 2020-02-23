#import flask
from flask import Flask, jsonify
import numpy as np
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
 
#create app
app = Flask(__name__)
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new 

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)


# Save reference to the table
Station = Base.classes.Station
Measurement = Base.classes.Measurement



# Define static routes
@app.route("/")
def home():

    return (
        f"Hawaii Weather Data:<br/>"
        f"Choose from routes below:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/<start><br/><br/>"
        f"/api/v1.0/<start>/<end><br/><br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
	stations = (session
							.query(Station).all())

	list_station = list()
	for station in stations:
			stations_dict = dict()
			stations_dict['Station'] = station.station
			stations_dict['Station Name']= station.name
			list_station.append(stations_dict)

	return jsonify (list_station)

@app.route("/api/v1.0/tobs")
def tobs():
  	active_temps = (session
							.query(Measurement.tobs,Measurement.date,Measurement.station)
							.filter(Measurement.date > active_station)
							.all())

	temp_list = list()
	for data in active_temps:
			temp_dict = dict()
			temp_dict['Station'] = data.station
			temp_dict['Date'] = data.date
			temp_dict['Temp'] = data.tobs
			temp_list.append(temp_dict)

	return jsonify (temp_list)  

@app.route("`/api/v1.0/<start>`")
def start(start=None):

	start_temps = session.query(
			func.min(Measurement.tobs), 
		   	func.avg(Measurement.tobs),
			func.max(Measurement.tobs)
	).filter(
			Measurement.date >= start
	).all()


	temp_stats = list()
	for tmin, tavg, tmax in start_temps:
		temp_stats_dict = {}
		temp_stats_dict["Min Temp"] = tmin
		temp_stats_dict["Max Temp"] = tavg
		temp_stats_dict["Avg Temp"] = tmax
		temp_stats.append(temp_stats_dict)

	return jsonify (temp_stats)


@app.route ("`/api/v1.0/<start>/<end>`")
def calc_temps(start=None,end=None):
    temp = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(
    	Measurement.date >= start,
    	Measurement.date <= end
    ).all()

    start_end = list()
    for tmin, tavg, tmax in temp:
    	 start_end_dict = dict()
    	 start_end_dict["Min Temp"] = tmin
    	 start_end_dict["Avg Temo"] = tavg
    	 start_end_dict["Max Temp"] = tmax
    	 start_end.append(start_end_dict)

    return jsonify (start_end)
  
if __name__ == '__main__':
    app.run(debug=True)