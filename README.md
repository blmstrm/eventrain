EventRain
===

EventRain is a framework enabling reporting and broadcasting of user-generated events through mobile devices.

Android:
The Android client is built using fragments, one fragment representing the Map view and another fragment representing the event-reporting view.

Server:
The server is built using Python and Redis along with GCM for message sending to Android devices.

Usage
===
First make sure that an instance of Redis is running.

To start the server component run the python script:
````
python er_server.py
````


to be continued...

TODO
===
General
* Add more detail to this README.
* Describe android usage.

Server
* Add support for regions in server.
* Add correct parsing of longitude/latitude.
* Add support for GCM.
* Add configuration file for settings.
* Add a resonable data structure for device identification.
* Add a resonable data structure for location information.
* Add support for several clients.
* Concentrate everything in an API.
* Add proper sub/pub channels.
* Merge both python scripts into one.

Android application
* Add sensible picture to report event ImageButton.
* Add support for GCM intents.
* Add configuration file for server information etc.
* 


