SELECT
MIN(tobs) as TMIN, 
AVG(tobs) as TAVG, 
MAX(tobs) as TMAX
FROM Measurement
WHERE date >= '{start_date}';