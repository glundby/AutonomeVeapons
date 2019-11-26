#!/user/bin/python3

# Parameters for size of War Theater Square

import numpy as np
import gmplot

# Dal:
fromLat = 60.0
fromLon = 11.0
hArea =  16.0  # Km Northward 
wArea =  25.0  # Km Eastward

# Kongsvinger
# fromLat = 60.245676
# fromLon = 11.981047
# hArea =  40.0  # Km Northward
# wArea =  10.0  # Km Eastward

# Tana
# fromLat = 70.07
# fromLon = 28.00
# hArea = 50
# wArea = 8

# Google map key:  AIzaSyCgYgSUGCBI5oxHEW-X_AXDBCj668Ei9zY

# Operational Theatre
hA = hArea/1.11/100                           # Km to fractional deg
wA = wArea/1.11/100/np.cos(fromLat/360*6.28)  # convert Lat to radians

gmap1 = gmplot.GoogleMapPlotter(fromLat+hA/2, fromLon+wA/2, 12)  # zoom level last
