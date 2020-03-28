from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather


class WeatherStation:

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