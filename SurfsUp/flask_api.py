import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route('/')
def welcome():
    return (
        f"<h1>Available Routes:<br/></h1>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt start &gt <br/>"
        f"/api/v1.0/&lt start &gt/&lt end &gt"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Query date and precipitation in the last 12 months
    precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in precip_scores:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query a list of stations
    station = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()
    
    # Create a list
    station_list = []
    for sta in station:
        sta = tuple(sta)
        station_list.append(sta)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year of data
    temps_one_year = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == "USC00519281").\
                filter(Measurement.date >= '2016-08-23').all()
    
    session.close()

    # Create a list of dictionary
    temps_date = []
    for date, tobs in temps_one_year:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temps_date.append(temp_dict)

    return jsonify(temps_date)

@app.route("/api/v1.0/<start>")
def customize_start(start):
    with open("customize_start.sql") as file:
            statement = file.read()
            statement = statement.format(start_date=start)
            print(statement)
            # alternative to: result = engine.execute(statement)
            with engine.connect() as conn:
                result = conn.execute(text(statement))
            
            start_temps = []
            for min, avg, max in result:
                temp_dict = {}
                temp_dict["TMIN"] = min
                temp_dict["TAVG"] = avg
                temp_dict["TMAX"] = max
                start_temps.append(temp_dict)
            return jsonify(start_temps)
    
@app.route("/api/v1.0/<start>/<end>")
def customize_start_end(start, end):
    with open("customize_start_end.sql") as file2:
            statement2 = file2.read()
            statement2 = statement2.format(start_date=start, end_date=end)
            print(statement2)
  
            with engine.connect() as conn:
                result2 = conn.execute(text(statement2))
            
            start_end_temps = []
            for min, avg, max in result2:
                temp_dict2 = {}
                temp_dict2["TMIN"] = min
                temp_dict2["TAVG"] = avg
                temp_dict2["TMAX"] = max
                start_end_temps.append(temp_dict2)
            
            return jsonify(start_end_temps)

if __name__ == '__main__':
    app.run(debug=True)