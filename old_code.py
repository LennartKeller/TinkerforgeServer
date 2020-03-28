ipcon.set_timeout(30)

    while True:

    # ----- connection state ausgeben
        if ipcon.get_connection_state():
            print("connection ok")
            fix, satellites = gps.get_status()
            latitude, ns, longitude, ew = gps.get_coordinates()
            heading, speed = gps.get_motion()
            alt, geosep = gps.get_altitude()
            voltage_usb, voltage_dc = hat.get_voltages()
            chip_temperature_hat = hat.get_chip_temperature()
            temperature, humidity, last_change = wea.get_sensor_data(83)
            motion = mot.get_motion_detected()
            chip_temperature_mot = mot.get_chip_temperature()
        else:
            print("no connection!")

# Berechnung Entfernung
        if lon2 > 0:
            lon1 = longitude/1000000.0
            lat1 = latitude/1000000.0
            R = 6371000  # // radius of the earth in meter
            x = (math.radians(lon2) - math.radians(lon1)) * math.cos( 0.5*(math.radians(lat2)+math.radians(lat1)) )
            y = math.radians(lat2) - math.radians(lat1)
            d = R * math.sqrt( x*x + y*y )
            lon2 = lon1
            lat2 = lat1
        else:
            lon2 = longitude/1000000.0
            lat2 = latitude/1000000.0



        print("Schleife: " + str(count))
        print()
        if fix:
            print("GPS-Data")
            print("  GPS is fixed")
            print("  Satellites            : " + str(satellites))
            print("  Latitude              : " + str(latitude/1000000.0) + " °" + ns)
            print("  Longitude             : " + str(longitude/1000000.0) + " °" + ew)
            print("  Speed                 : " + str(speed/100))
            if d < 1000:
                print("  Entfernung            : " + str(d) + " m")
            else:
                print("  Entfernung            : " + str(d/1000.0) + " km")
        else:
            print("No GPS fix!")
        print()
        print("HAT-Data")
        print("  Eingangsspannung (USB): " + str(voltage_usb/1000.0) + " V")
        print("  Eingangsspannung (DC) : " + str(voltage_dc/1000.0) + " V")
        print("  Temperatur (CPU)      : " + str(chip_temperature_hat) + " °C")
        print()
        print("Wetter-Sensor")
        print("  Temperatur            : " + str(temperature/10) + " °C")
        print("  Luftfeuchte           : " + str(humidity) + "%")
        print("  Letzte Änderung vor   : " + str(last_change/60.0) + " Minuten")
        print()
        print("Motion Detector")
        if motion:
            print("  Bewegung!")
        else:
            print("  Alles ruhig!")
        print("  Temepratur (CPU)      : " + str(chip_temperature_mot) + " °C")
        count = count + 1
        print()

        # ----- Pushover-Meldung ausgeben
        if temperature < 30:
            t_count = t_count + 1
            if t_count < 6:
                client.send_message("Frostgefahr! " + str(temperature/10) + " °", title = "Tinker")
        else:
            t_count = 0
        if motion:
            client.send_message("Es bewegt sich was!", title = "Tinker")

        # ----- Daten an Traccar-Server senden
        if speed > 100:
            try:
                speed = speed/1.852
                r = requests.get("http://4kellers.no-ip.info:5055/?id=123456&lat=" + str(latitude/1000000.0) + "&lon=" + str(longitude/1000000.0) + "&altitude=" + str((alt+geosep)/100.0) + "&speed=" + str(speed/100.00) + "&volt=" + str(voltage_dc/1000.0) + "&Temp=" + str(temperature/10) + "&Humidity=" + str(humidity), timeout=1)
            except Exception as e:
                print('The request timed out')
                print (e)
            else:
                print('The request did not time out')
                print(r)
        time.sleep(10)
    ipcon.disconnect()
    time.sleep(1)