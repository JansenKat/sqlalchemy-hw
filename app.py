from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Resources/hawaii.sqlite'
db = SQLAlchemy(app)

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(getattr(self, column.name), datetime.datetime)
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class Measurement(db.Model, DictMixIn):
    __tablename__ = "measurement"

    date = db.Column(db.Date(), primary_key=True)
    station = db.Column(db.String())
    prcp = db.Column(db.Integer())
    tobs = db.Column(db.Integer())

class Station(db.Model, DictMixIn):
    __tablename__ = "station"

    station = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    latitude = db.Column(db.Integer())
    longitude = db.Column(db.Integer())
    elevation = db.Column(db.Integer())

meas_cols = ['date','statino','prcp','tobs']
station_cols = ['station','name','latitude','longitude','elevation']


@app.route('/')
def home():
    #list of links to other routes
    return render_template("index.html")

@app.route('/api/v1.0/precipitation')
def prcp():
    #Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    #Return the JSON representation of your dictionary.
    prcp = db.session.query(Measurement.date,Measurement.prcp).all()
    return jsonify([list(p) for p in prcp])


@app.route('/api/v1.0/stations')
def station():
    #Return a JSON list of stations from the dataset.
    stat = db.session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    return jsonify([dict(zip(station_cols,list(s))) for s in stat])


@app.route('/api/v1.0/tobs')
def tobs():
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    tobs = db.session.query(Measurement.date,Measurement.tobs).all()
    return jsonify([list(tob) for tob in tobs])


@app.route('/api/v1.0/<start>')
def start():
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    return


@app.route('/api/v1.0/<start>/<end>')
def end():
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    return


if __name__ == "__main__":
    app.run(debug=True)