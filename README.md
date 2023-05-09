# sqlalchemy-challenge
## Challenge Information
### This challenge was divided into two parts. The first part involves the analysis of the climate data of Honolulu, Hawaii, using Python and SQLAlchemy. The analysis was carried out in Jupyter Notebook (file name: climate.ipyb).

### The second part of the challenge involves the design of a Flask API based on the queries that were developed. The following routes were included in the Flask API:
- "/" returns homepage
- "/api/v1.0/precipitation" returns a JSON representation of the previous precipitation analysis
- "/api/v1.0/stations" returns a JSON list of stations
- "/api/v1.0/tobs" returns a JSON list of temperature observation in the most recent year of the dataset
- "/api/v1.0/<start>" and "/api/v1.0/<start>/<end>" returns a JSON list of the minimum temperature (TMIN), the average temperature (TAVG) and the maximum temperature (TMAX), based on the start date and/or the end data which the user specify in the URL
### The Flask application can be found in file: flask_api.py. The SQL queries for the last API route can be found in documents: customize_start.sql and customize_start_end.sql.