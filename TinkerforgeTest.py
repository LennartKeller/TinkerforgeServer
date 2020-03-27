HOST = "localhost"
PORT = 4223
UID_GPS = "GPS" # Change XYZ to the UID of your GPS Bricklet 2.0
UID_HAT = "JXG"
UID_WEA = "K2g"
UID_MOT = "J9X"


from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge.brick_hat import BrickHAT
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from TinkerforgeServer import ObjectServer

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    gps = BrickletGPSV2(UID_GPS, ipcon) # Create device objects
    hat = BrickHAT(UID_HAT, ipcon)
    wea = BrickletOutdoorWeather(UID_WEA, ipcon)
    mot = BrickletMotionDetectorV2(UID_MOT, ipcon)
    ipcon.connect(HOST, PORT) # Connect to brickd

    # add objects to server

    server = ObjectServer()
    server.add(gps)
    server.add(hat)
    server.add(wea)
    server.add(mot)