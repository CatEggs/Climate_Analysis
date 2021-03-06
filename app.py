from flask import Flask, jsonify, request
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind=engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"<h1><center>Welcome to Surf's Up</center></br></h1>"
        f"<center><h3>/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start</br>"
        f"/api/v1.0/start/end</br></h3></center>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(Measurement.prcp, Measurement.date).all()
    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # List of Stations
    station_data = (
        session.query(Measurement.station).distinct(Measurement.station).all()
    )
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Last 12 months of temp observations
    last_yr = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    tobs_data = (
        session.query(Measurement.station, Measurement.tobs, Measurement.date)
        .filter(Measurement.date >= last_yr)
        .all()
    )
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def calc_temps(start):
    temp_data = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def calc_temps_full(start, end):

    temp_data = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )
    return jsonify(temp_data)


if __name__ == "__main__":
    app.run(debug=True)
