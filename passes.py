#!/usr/bin/env python3
import skyfield
from skyfield.api import load, wgs84
import numpy as np
from pprint import pprint

# Locations
oz1sej = wgs84.latlon(55.7852261, 12.325613, elevation_m=30) # Kirke Værløse
oz1sct = wgs84.latlon(55.4296559, 11.558497, elevation_m=30) # Sorø

print()
print("**************************************************************")
print("Remember to check http://ub8qbd.satdump.org/wx_report_new.html")
print("**************************************************************")

ts = load.timescale()
t0 = ts.now()
t1 = t0 + 1 # NUMBER OF DAYS INTO THE FUTURE

# Satellites

sats = []

satList = []
satList.append("NOAA 15")
satList.append("NOAA 18")
satList.append("NOAA 19")
satList.append("METEOR-M 2")
satList.append("METEOR-M2 2")
satList.append("ISS (ZARYA)")

file = 'http://celestrak.org/NORAD/elements/satnogs.txt'
satellites = load.tle_file(file) # SET reload=True FOR REAL APPLICATIONS!

by_name = {sat.name: sat for sat in satellites}

for satName in satList:
    sats.append(by_name[satName])
    epoch = by_name[satName].epoch
    if  t0-epoch > 7:
        print("WARNING! Epoch of satellite",satName,"is",t0-epoch,"days old!")
    else:
        print(f"{satName:15s}","epoch is",f"{t0-epoch:3.1f}","days old")

print("*************************************")
print()
print( f"{'TIME (UTC)':25s} {'SATELLITE':15s} {'φₘₐₓ':20s}")
print("-------------------------------------------------------")
passes = np.empty((0,5), float)

eph = load("de421.bsp")
    
i=0
for sat in sats:
    t, events = sat.find_events(oz1sej, t0, t1) # FIND EVENTS FOR THIS LOCATION
    difference = sat - oz1sej
    for ti, event in zip(t, events):
        if event == 1: # Only show culmination, not rise or set
            topocentric = difference.at(ti)
            alt, az, distance = topocentric.altaz()
            if alt.degrees > 45: # MINIMUM ELEVATION TO SHOW
                sun = topocentric.is_sunlit(eph)
                passes = np.append(passes, np.array([[ti,ti.tai,sat.name,alt,sun]]), axis=0)
    i=i+1

passes2 = passes[passes[:,1].argsort()]

for satpass in passes2:
    time = satpass[0].utc_strftime('%Y %b %d %H:%M:%S')
    name = satpass[2]
    maxe = str(round(satpass[3].degrees)) + "°"
    ecli = "(eclipsed)" if not sun else ""
    print( f"{time:25s} {name:15s} {maxe:5s}",ecli)

print()