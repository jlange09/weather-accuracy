import tornado.web

from dominate.tags import *

class WeatherViewHandler(tornado.web.RequestHandler):
    def get(self):
        # Build the web page
        _html = html()
        _head = _html.add(head(title("Weather Forecast Accuracy")))
        _head += script(type='text/javascript', src='/static/scripts/jquery.js')
        _head += script(type='text/javascript', src='/static/scripts/jquery.flot.js')
        _head += script(type='text/javascript', src='/static/scripts/jquery.flot.time.js')
        _head += script(type='text/javascript', src='/static/scripts/jquery.flot.navigate.js')
        _head += script(type='text/javascript', src='/static/scripts/weathergraphs.js')
        _head += link(rel='stylesheet', type='text/css', href='/static/css/weather.css')
        _body = _html.add(body())

        # Forecast/temp lines...
        graphs_div = _body.add(div(_class='main'))
        graphs_div.add(div(id='temp_graph', _class='graph'))

        # Delta lines
        graphs_div.add(div(id='temp_delta_graph', _class='graph'))

        self.write(str(_html))
