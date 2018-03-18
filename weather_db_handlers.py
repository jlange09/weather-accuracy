from db_helpers import *

class WeatherDbHandler(PostgresDbHandler):
    def __init__(self):
        self.database = 'weather'
        self.set_common_write_details()

    @staticmethod
    def create_collection_record(conn):
        querystr = "INSERT INTO collection_times (date_taken) values (now()) RETURNING collection_id"
        with closing(conn.cursor()) as cursor:
            cursor.execute(querystr)
            collection_id = cursor.fetchone()[0]

            return collection_id
