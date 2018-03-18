import urllib2
import json

from contextlib import closing
from time import gmtime, strftime
from weather_db_handlers import *

# XXX TODO
# Fill in with your wunderground api key.
# query can be a city, or coordinates (e.g. 44,-122)
api_url = 'http://api.wunderground.com/api/myapikey/hourly10day/q/query.json'
with closing(urllib2.urlopen(api_url)) as hourly10dayurl:
    hourly10day = json.loads(hourly10dayurl.read())

with WeatherDbHandler().pooled_connection() as conn:
    collection_id = WeatherDbHandler.create_collection_record(conn)
    for forecast in hourly10day['hourly_forecast']:
        fcttime = forecast['FCTTIME']
        del forecast['FCTTIME']

        querystr = "INSERT INTO hourly_forecasts (collection_id, fcttime, forecast_data) values (%s, %s, %s) RETURNING forecast_id"
        with closing(conn.cursor()) as cursor:
            cursor.execute(querystr, (collection_id, json.dumps(fcttime), json.dumps(forecast)))
            forecast_id = cursor.fetchone()[0]
            print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Inserted hourly forecast data with id %d for collection id %d" % (forecast_id, collection_id)
    conn.commit()
