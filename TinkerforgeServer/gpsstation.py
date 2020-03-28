import math
from tinkerforge.bricklet_gps_v2 import BrickletGPSV2


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
        return alittude - geoidal_separation


