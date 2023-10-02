import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session 
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    return(
        "Welcome to the Climate Analysis Project<br/>"
        "Available Routes: <br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date<br/>"
        "/api/v1.0/start_date/end_date"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    a_year_ago = dt.date(2017,8,23) - dt.timedelta(365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    session.close()
    precipitation_dict = {}
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp
    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def station():
    station_data = session.query(Station.station).all()
    station_list = list(np.ravel(station_data))
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    a_year_ago = dt.date(2017,8,23) - dt.timedelta(365)
    temperature_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year_ago).all()
    session.close()
    temperature_list = list(np.ravel(temperature_data))
    return jsonify(temperature_list)

@app.route('/api/v1.0/<start>')
def start_date(start):
    start_date = start

    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    temperature_dict = {
        'TMIN': temperature_stats[0][0],
        'TAVG': temperature_stats[0][1],
        'TMAX': temperature_stats[0][2]
    }

    return jsonify(temperature_dict)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    start_date = start
    end_date = end

    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    temperature_dict = {
        'TMIN': temperature_stats[0][0],
        'TAVG': temperature_stats[0][1],
        'TMAX': temperature_stats[0][2]
    }

    return jsonify(temperature_dict)


if __name__ == "__main__":
    app.run()