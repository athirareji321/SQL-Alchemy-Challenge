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
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Querying the most recent date column of the Measurement table and converting todate type
    a_year_ago = dt.date(2017,8,23) - dt.timedelta(365)
    
    # Querrying date and precipitation columns from the measurement tables         
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= a_year_ago).all()
    session.close()
    
    # Converting the results into a dictionary     
    precipitation_dict = {}
    
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp
        
    # Returing the results as a JSON         
    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def station():

    # Querrying station columns from the station tables 
    station_data = session.query(Station.station).all()
    station_list = list(np.ravel(station_data))
    
    # Returing the results as a JSON  
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    # Querying the most recent date column of the Measurement table and converting todate type
    a_year_ago = dt.date(2017,8,23) - dt.timedelta(365)
    
    # Querying the data for the ost active station for the last one year and closing the session
    temperature_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year_ago).all()
    session.close()
    
    # Converting the results into a list and returing the results as a JSON
    temperature_list = list(np.ravel(temperature_data))
    return jsonify(temperature_list)

@app.route('/api/v1.0/<start>')
def start_date(start):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)     
    
    start_date = start
    
    # Querying for TMIN, TAVG, and TMAX for the given start date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    # Converting the results into a list and returing the results as a JSON
    temperature_dict = {
        'TMIN': temperature_stats[0][0],
        'TAVG': temperature_stats[0][1],
        'TMAX': temperature_stats[0][2]
    }
    return jsonify(temperature_dict)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_date = start
    end_date = end
    
    # Querying for TMIN, TAVG, and TMAX in between the given start and end date
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # Converting the results into a list and returing the results as a JSON
    temperature_dict = {
        'TMIN': temperature_stats[0][0],
        'TAVG': temperature_stats[0][1],
        'TMAX': temperature_stats[0][2]
    }

    return jsonify(temperature_dict)


if __name__ == "__main__":
    app.run()