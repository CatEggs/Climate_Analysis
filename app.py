from flask import Flask, jsonify, request

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
    f"/api/v1.0/start/end</br></h3></center>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = (session.query(Measurement.prcp, Measurement.date).all())
    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
# List of Staions
    station_data = (
    session.query(Measurement.station).distinct(Measurement.station).all()
)
    return jsonify(station_data)

if __name__ == "__main__":
    app.run(debug=True)