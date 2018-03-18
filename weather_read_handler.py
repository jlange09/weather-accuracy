import json
import tornado.web

from db_helpers import *
from contextlib import closing

class WeatherReadDbHandler(PostgresDbHandler):
    def __init__(self):
        self.pooled_conns = Queue.LifoQueue(5)
        self.database = 'weather'
        self.set_common_read_details()

global_weather_read_handler = WeatherReadDbHandler()

class WeatherReqHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        with global_weather_read_handler.pooled_connection() as conn:
            with closing(conn.cursor()) as cursor:
                query = ("select extract(epoch from date_taken), json_agg(json_build_object('forecast_epoch', fcttime::json->>'epoch', 'forecast_temp', forecast_data::json#>>'{temp,english}') order by fcttime::json->>'epoch') from hourly_forecasts join collection_times using (collection_id) where date_taken between now()-interval '10 days' and now() and cast(fcttime::json->>'epoch' as float) between extract(epoch from now() - interval '10 days') and extract(epoch from now()) group by date_taken order by date_taken")
                forecast_data = []
                cursor.execute(query)
                for (collection_epoch, forecast_data_for_collection) in cursor:
                    forecast_data.append({"collection_epoch":collection_epoch, "forecast":forecast_data_for_collection})

            with closing(conn.cursor()) as cursor:
                query = ("select observation_data::json->>'observation_epoch' as observation_epoch, avg(cast(observation_data::json->>'temp_f' as float)) as measured_temp from current_observations group by observation_data::json->>'observation_epoch' order by observation_data::json->>'observation_epoch'")
                observation_data = []
                cursor.execute(query)
                for (observation_epoch, measured_temp) in cursor:
                    observation_data.append({"observation_epoch":observation_epoch, "measured_temp":measured_temp})

        self.write(json.dumps({"collected_forecasts":forecast_data, "observation_data":observation_data}))
