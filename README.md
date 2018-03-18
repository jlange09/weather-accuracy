# weather-accuracy
Tracks observation and forecast data and plots various graphs showing accuracy

# Getting Started
1. This requires a backing database. The schema used in the sample code is in schema.sql.
2. To run the forecast/observation collection I'm using a simple cron job:
```
0 * * * * ( python ~/forecast_collection.py &>> ~/forecast-collection.log )
*/5 * * * * ( python ~/weather_collection.py &>> ~/weather-collection.log )
```
Obviously you could launch the collection scripts and have them run a loop if that's easier.

3. Copy all .sample files to a new file with the .sample removed, and modify the code at each of the TODO markers as necessary
4. Running app.py should be the entry point for the web server.

Optionally, you may want to consider a log rotation job in /etc/logrotate.conf:
```
/home/youruser/*.log {
    create 0600 youruser yourgroup
    copytruncate
    daily
    rotate 10
    compress
    missingok
    notifempty
}
```
