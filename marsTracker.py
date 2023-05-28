#!/usr/bin/env python3
import skyfield
from skyfield.api import load, wgs84
import time

# Locations
oz1sej = wgs84.latlon(55.7852261, 12.325613, elevation_m=30) # Kirke Værløse
oz1sct = wgs84.latlon(55.4296559, 11.558497, elevation_m=30) # Sorø

print()
print("**************************************************************")

eph   = load("de421.bsp")
ts    = load.timescale()
mars  = eph["mars"]
earth = eph["earth"]

mypos = oz1sej + earth
diff  = mars - mypos

print("Elevation   Azimuth    Distance")
while True:
    now   = ts.now()
    astro = mypos.at(now).observe(mars)
    app   = astro.apparent()
    alt, az, distance = app.altaz()
    print(f"{alt.degrees:3.4f}     {az.degrees:3.4f}   {distance}")
    time.sleep(1)
