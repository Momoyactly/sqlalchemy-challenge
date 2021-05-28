from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# SQLalqchemy Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station =  Base.classes.station
#################################################
# Flask Routes
#################################################
session = Session(engine)
newest = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
oneYearLess = dt.datetime.strptime(newest, '%Y-%m-%d')-dt.timedelta(days=365)
session.close()

@app.route("/")
def home():
    return "Hi"

@app.route("/api/v1.0/precipitation")
def precipitation():
    '''Convert the query results to a dictionary using date as the key and prcp as the value.'''
    session = Session(engine)
    response = {}
    for row in session.query(measurement.date, measurement.prcp).all():
        response[row[0]]=row[1]
    session.close()
    return jsonify(response)


@app.route("/api/v1.0/stations")
def stations():
    '''Return a JSON list of stations from the dataset.'''
    session = Session(engine)
    response = []
    for row in session.query(station.name).all():
        response.append(row[0])
    session.close()
    return jsonify(response)


@app.route("/api/v1.0/tobs")
def tobs():
    '''Return a JSON list of stations from the dataset.'''
    session = Session(engine)
    response = {}
    data = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > oneYearLess).\
        filter(measurement.station == 'USC00519281').all()
    for row in data:
        response[row[0]]=row[1]
    session.close()
    return jsonify(response)


@app.route("/api/v1.0/<start>")
def stats(start):
    '''Return a JSON list of stations from the dataset.'''
    session = Session(engine)
    response = []
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    data = session.query(*sel).\
        filter(measurement.date > start).all()
    for row in data:
        response.append({'Min':row[0],'Max':row[1],'Avg':row[2]})
    session.close()
    return jsonify(response)


@app.route("/api/v1.0/<start>/<end>")
def stats_range(start,end):
    '''Return a JSON list of stations from the dataset.'''
    session = Session(engine)
    response = []
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    data = session.query(*sel).\
        filter(measurement.date > start).\
            filter(measurement.date < end).all()
    for row in data:
        response.append({'Min':row[0],'Max':row[1],'Avg':row[2]})
    session.close()
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
