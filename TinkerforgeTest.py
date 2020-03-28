from tinkerforge.brick_hat import BrickHAT
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from tinkerforge.ip_connection import IPConnection
from TinkerforgeServer.objectserver import ObjectServer

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


class TinkerforgeWeatherStation:

    def __init__(self, bricklet: BrickletOutdoorWeather):
        if not isinstance(bricklet, BrickletOutdoorWeather):
            raise Exception('Bricklet-Object has to be of type {}'.format(type(BrickletOutdoorWeather)))
        self.bricklet = bricklet

    def get_temperature(self) -> float:
        """
        Returns the temperature in celcius.
        :return: degree celcius as float
        """
        temperature, humidity, last_change  = self.bricklet.get_sensor_data(83)
        return temperature/10

    def get_humidity(self) -> float:
        """
        Returns the humidity in percentage.
        :return: humidity as float
        """
        temperature, humidity, last_change = self.bricklet.get_sensor_data(83)
        return humidity

    def get_last_change(self) -> float:
        """
        Returns the time in minutes since last change of weather data
        :return: time since last change in minutes
        """
        temperature, humidity, last_change = self.bricklet.get_sensor_data(83)
        return last_change / 60

if __name__ == "__main__":

    ipcon = IPConnection()  # Create IP connection
    gps = BrickletGPSV2(UID_GPS, ipcon)  # Create device objects
    hat = BrickHAT(UID_HAT, ipcon)
    wea = BrickletOutdoorWeather(UID_WEA, ipcon)
    mot = BrickletMotionDetectorV2(UID_MOT, ipcon)
    ipcon.connect(HOST, PORT)  # Connect to brickd

    if ipcon.get_connection_state():
        server = ObjectServer()
        weatherstation = TinkerforgeWeatherStation(wea)
        server.register(weatherstation)
        server.run(host='0.0.0.0', port='8080')
    else:
        print("Connection to Tinkerforge failed")
