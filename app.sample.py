import tornado.ioloop
import tornado.web
import tornado.httpserver

# Views
from weather_view import *

# Read handlers
from weather_read_handler import *

from tornado.log import enable_pretty_logging

application = tornado.web.Application(handlers = [
    (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': r'./static/images/'}),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': r'./static/'}),
    ("/weather", WeatherViewHandler),
    ("/read/weather", WeatherReqHandler)
])

# XXX TODO Configure ssl as necessary, or remove ssl options
http_server = tornado.httpserver.HTTPServer(application,
    ssl_options={
        "certfile": "/etc/letsencrypt/live/path/to/fullchain.pem",
        "keyfile": "/etc/letsencrypt/live/path/to/privkey.pem"
    },
    no_keep_alive=True,
    idle_connection_timeout=300
)

if __name__ == "__main__":
    enable_pretty_logging()
    http_server.listen(8443)
    tornado.ioloop.IOLoop.instance().start()
