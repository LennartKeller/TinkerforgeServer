from tinkerforge.brick_hat import BrickHAT
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from tinkerforge.ip_connection import IPConnection

from TinkerforgeServer import ObjectServer
from TinkerforgeServer import TinkerforgeWeatherStation, GPSStation

# CONSTANTS
HOST = "localhost"
PORT = 4223
UID_GPS = "GPS"  # Change XYZ to the UID of your GPS Bricklet 2.0
UID_HAT = "JXG"
UID_WEA = "K2g"
UID_MOT = "J9X"

# create tinkerforge objects
ipcon = IPConnection()  # Create IP connection
gps = BrickletGPSV2(UID_GPS, ipcon)  # Create device objects
hat = BrickHAT(UID_HAT, ipcon)
wea = BrickletOutdoorWeather(UID_WEA, ipcon)
mot = BrickletMotionDetectorV2(UID_MOT, ipcon)
ipcon.connect(HOST, PORT)  # Connect to brickd



if __name__ == "__main__":

    ipcon = IPConnection()  # Create IP connection
    gps = BrickletGPSV2(UID_GPS, ipcon)  # Create device objects
    hat = BrickHAT(UID_HAT, ipcon)
    wea = BrickletOutdoorWeather(UID_WEA, ipcon)
    mot = BrickletMotionDetectorV2(UID_MOT, ipcon)
    ipcon.connect(HOST, PORT)  # Connect to brickd

    if ipcon.get_connection_state():
        weatherstation = TinkerforgeWeatherStation(wea)
        gpsstation = GPSStation(gps)

        server = ObjectServer(filter_privates=True)
        server.register(weatherstation)
        server.register(gpsstation)
        server.run(host='0.0.0.0', port='8080')
    else:
        print("Connection to Tinkerforge failed")
