import urllib2
import json

from contextlib import closing
from time import gmtime, strftime
from weather_db_handlers import *

# XXX TODO
# Fill in with your wunderground api key.
# query can be a city, or coordinates (e.g. 44,-122)
api_url = 'http://api.wunderground.com/api/myapikey/conditions/q/query.json'
with closing(urllib2.urlopen(api_url)) as conditionsurl:
    conditions = json.loads(conditionsurl.read())

with WeatherDbHandler().pooled_connection() as conn:
    collection_id = WeatherDbHandler.create_collection_record(conn)
    display_location = conditions['current_observation']['display_location']
    observation_location = conditions['current_observation']['observation_location']
    del conditions['current_observation']['display_location']
    del conditions['current_observation']['observation_location']
    del conditions['current_observation']['image']

    querystr = "INSERT INTO current_observations (collection_id, display_location, observation_location, observation_data) values (%s, %s, %s, %s) RETURNING observation_id"
    with closing(conn.cursor()) as cursor:
        cursor.execute(querystr, (collection_id, json.dumps(display_location), json.dumps(observation_location), json.dumps(conditions['current_observation'])))
        observation_id = cursor.fetchone()[0]
        print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Inserted current observation data with id %d for collection id %d" % (observation_id, collection_id)
    conn.commit()
