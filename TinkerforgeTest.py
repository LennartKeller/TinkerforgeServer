HOST = "localhost"
PORT = 4223
UID_GPS = "GPS" # Change XYZ to the UID of your GPS Bricklet 2.0
UID_HAT = "JXG"
UID_WEA = "K2g"
UID_MOT = "J9X"

count = 1 # counter Schleifen
t_count = 0 #counter Temperatur Warnung
lon2 = 0 # longitude
lat2 = 0 # Latitude
d = 0 # Entfernung

import requests
import time
import math

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge.brick_hat import BrickHAT
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from pushover import Client
from requests.exceptions import Timeout

# Token für pushover
client = Client ("u9yMhUgytePtkw9W6wMjWhG6GuyFiE", api_token="aopj7djwr7degpd2vw3e8pc5gmy5aq")

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    gps = BrickletGPSV2(UID_GPS, ipcon) # Create device objects
    hat = BrickHAT(UID_HAT, ipcon)
    wea = BrickletOutdoorWeather(UID_WEA, ipcon)
    mot = BrickletMotionDetectorV2(UID_MOT, ipcon)
    ipcon.connect(HOST, PORT) # Connect to brickd