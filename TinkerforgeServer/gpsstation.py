import math
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from typing import Tuple


class GPSStation:

    def __init__(self, bricklet: BrickletGPSV2):
        if not isinstance(bricklet, BrickletGPSV2):
            raise Exception('Bricklet-Object has to be of type {}'.format(type(BrickletGPSV2)))
        self.bricklet = bricklet

    def has_fix(self) -> bool:
        fix, n_satelites = self.bricklet.get_status()
        return fix

    def get_satelites(self) -> int:
        fix, n_satelites = self.bricklet.get_status()
        return n_satelites

    def get_course(self) -> float:
        if not self.has_fix():
            return math.nan
        course, speed = self.bricklet.get_motion()
        return course

    def get_speed(self) -> float:
        if not self.has_fix():
            return math.nan
        course, speed = self.bricklet.get_motion()
        return speed / 100

    def get_altitude(self) -> float:
        if not self.has_fix():
            return math.nan
        alittude, geoidal_separation = self.bricklet.get_altitude()
        return (alittude - geoidal_separation) / 100

    def get_longitude(self) -> Tuple[float, str]:
        if not self.has_fix():
            return math.nan
        latitude, ns, longitude, ew = self.bricklet.get_coordinates()
        return longitude / 1000000, ew

    def get_latitude(self) -> Tuple[float, str]:
        if not self.has_fix():
            return math.nan
        latitude, ns, longitude, ew = self.bricklet.get_coordinates()
        return latitude / 1000000, ns

    def get_coordinates(self) -> Tuple[float, str, float, str]:
        latitude, ns, longitude, ew = self.bricklet.get_coordinates()
        latitude, longitude = latitude / 1000000, longitude / 1000000
        return latitude, ns, longitude, ew

    def get_chip_temperature(self):
        return self.bricklet.get_chip_temperature()

