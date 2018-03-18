import sys
import Queue
import psycopg2

from contextlib import contextmanager
from contextlib import closing

class PostgresDbHandler(object):
    # XXX TODO
    # Modify default values as necessary
    host = '/tmp/'
    port = None
    user = None
    database = 'postgres'
    schema = 'public'
    password = None
    is_read = False

    def set_db_creds(self):
        # XXX TODO
        # However you want to obtain your credentials should go here.
        # If on EC2, I recommend following: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html
        
    def set_common_read_details(self):
        # XXX TODO
        # Set host/port/creds as necessary
        self.host = None
        self.port = None
        self.set_db_creds()
        self.is_read = True

    def set_common_write_details(self):
        self.host = None
        self.port = None
        self.set_db_creds()
        self.is_read = False

    def do_get_connection(self):
        try:
            new_conn = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            """ From the pyscopg2 docs:
Warning By default, any query execution, including a simple SELECT will start a transaction: for long-running programs, if no further action is taken, the session will remain "idle in transaction", an undesirable condition for several reasons (locks are held by the session, tables bloat...). For long lived scripts, either ensure to terminate a transaction as soon as possible or use an autocommit connection.
            """
            if self.is_read:
                new_conn.autocommit = True

            with closing(new_conn.cursor()) as cursor:
                cursor.execute("SET SESSION SCHEMA '%s'" % self.schema)

            return new_conn
        except psycopg2.Error as err:
            print("Unhandled DB error")
            print(err)
            print("Trying to refresh creds...")
            sys.stdout.flush()
            self.set_db_creds()

            raise err

    @contextmanager
    def pooled_connection(self):
        available_conn = None
        try:
            available_conn = self.pooled_conns.get_nowait()

            with closing(available_conn.cursor()) as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception as e:
            print "No available connection (" + str(e) + "). Getting one..."
            sys.stdout.flush()

            if available_conn is not None:
                del available_conn
            
            # No pooled conn available, or pooled connection is dead.
            # Create one and rely on caller to return it
            available_conn = self.do_get_connection()

        try:
            yield available_conn
        finally: 
            try:
                self.pooled_conns.put_nowait(available_conn)
            except Queue.Full:
                # No need to add this back, queue is full
                del available_conn
