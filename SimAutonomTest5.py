#!/user/bin/python3
""" Test program for Autonome Veapons
https://www.color-hex.com/color-palette/84389"""

import gmplot
# Defined Classes for the simulation:
from SimAutonomVeapon5 import Rocket
from WarTheatre import generatewarmap
from AreaDef import fromLat, fromLon, hArea, wArea, hA, wA, gmap1
# Contains all the parameters to change for Simulation:
from AutonomeGlobals import simtime
# number of objects in simulation:
from AutonomeGlobals import numtanks, numheli, numinf, numactiveartillery
from AutonomeGlobals import rocketV1range, rocketV2range
from AutonomeGlobals import ammoinartbn
from AutonomeGlobals import numGRA  # ,numPH, PHrange, PHv0, PHhitrate
# Object container lists:
from AutonomeGlobals import tanks, helis, observers, bnobservers, artbns, panserhaubits
from AutonomeGlobals import rockets, infantry, activeartillery

# FUTURE IMPROVEMENT IS TO MAKE AN APP TO DEFINE WAR THEATER
# AND PLACE TARGETS OBSERVERS AND UNITS ON A GEOGRAPHIC MAP.
# IN THE MEANTIME WE MAKE A SQUARE AND PLACE ALL AT RANDOM

# Generate Targets, and Autonome veapons and place randomly

generatewarmap(fromLat, fromLon, hArea, wArea)             # Hides the nasty work
# May be changed to smarter interactive module
# May consider to store objects to run with same
for t in tanks:
    t.start()                # start targets  
print("started all Tanks")
for t in rockets:
    t.start()
print("started all Rockets")
for t in infantry:
    t.start()
print("Started all infantry companies")
for t in activeartillery:
    t.start()
print("Started all Active Artillery")
for t in helis:
    t.start()
print("Started all Helicopters")
for t in artbns:
    t.start()
print("Started ArtBns")
for t in panserhaubits:
    t.start()
print("Started all PanserHaubits")
for t in observers:         # lastly start observers to make target messages
    t.start()
for t in bnobservers:         # lastly start observers to make target messages
    t.start()
print("Started all Observers and BnObservers")

print("        All units have started simulation")
# Simulation runs..All in parallell
for t in panserhaubits:
    t.join()
print("All PanserHaubits finished")    
for t in observers:
    t.join()
print("All Observer finished")
for t in bnobservers:
    t.join()
print("All BnObserver finished")
for t in rockets:
    t.join()
print("All Rocket finished ")
for t in tanks:
    t.join()
print("All Tanks finished ")
for t in helis:
    t.join()
print("All Helis finished ")
for t in infantry:
    t.join()
print("All Infantries finished")
for t in activeartillery:
    t.join()
print("All ActiveArtillery finished")
for t in artbns:
    t.join()
print("All Art Bns finished")

print("All units have finished simulation time:", simtime, "minutes")

# Make statistic summary and result Maps!

helidestroyed = helidetected = tankdestroyed = tankdetected = infdestroyed = infdetected = 0
artdetected = artdestroyed = infhit = 0
print("")

marker_lats = []
marker_lngs = []
for t in tanks:
    if t.destroyed:
        tankdestroyed += 1
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
    if t.detected:
        tankdetected += 1
gmap1.scatter(marker_lats, marker_lngs, '#3B0B39', size=100, marker=False)

marker_lats = []
marker_lngs = []
for t in helis:
    if t.destroyed:
        helidestroyed += 1
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
    if t.detected:
        helidetected += 1
gmap1.scatter(marker_lats, marker_lngs, '#3B0B39', size=100, marker=False)

marker_lats = []
marker_lngs = []
for t in activeartillery:
    if t.destroyed:
        artdestroyed += 1
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
    if t.detected:
        artdetected += 1
gmap1.scatter(marker_lats, marker_lngs, '#3B0B39', size=100, marker=False)

marker_lats = []
marker_lngs = []
for t in infantry:
    if t.destroyed:
        infdestroyed += 1
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
    if t.detected:
        infdetected += 1
    if (t.strength < 100) and (t.strength > 50):
        infhit += 1
        gmap1.marker(t.Pos.latitude, t.Pos.longitude, '#3B0B39')  # Change colors later!
        print("inf company loss %:", (100 - t.strength))
gmap1.scatter(marker_lats, marker_lngs, '#3B0B39', size=300, marker=False)

# Write global Fire Map drawn of Autonome         
gmap1.apikey = "AIzaSyCgYgSUGCBI5oxHEW-X_AXDBCj668Ei9zY"
gmap1.draw("FireMap.html")

# lat_list = []
# lon_list = []
marker_lats = []
marker_lngs = []
gmap = gmplot.GoogleMapPlotter(fromLat+hA/2, fromLon+wA/2, 12)  # zoom level last
for t in infantry:
    if t.strength == 100:
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
gmap.heatmap(marker_lats, marker_lngs)
marker_lats = []
marker_lngs = []
for t in tanks:
    if not t.destroyed:
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
gmap.scatter(marker_lats, marker_lngs, '#ff0000', size=200, marker=False)
marker_lats = []
marker_lngs = []
for t in helis:
    if not t.destroyed:
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
gmap.scatter(marker_lats, marker_lngs, '#ff7b00', size=200, marker=False)

marker_lats = []
marker_lngs = []
for t in activeartillery:
    if not t.destroyed:
        marker_lats.append(t.Pos.latitude)
        marker_lngs.append(t.Pos.longitude)
gmap.scatter(marker_lats, marker_lngs, '#fff400', size=200, marker=False)

gmap.apikey = "AIzaSyCgYgSUGCBI5oxHEW-X_AXDBCj668Ei9zY"
gmap.draw("RestFiMap.html")

gmap = gmplot.GoogleMapPlotter(fromLat+hA/2, fromLon+wA/2, 12)  # zoom level last

marker_lats = []
marker_lngs = []
for t in rockets:
    if not t.fired:
        if t.range == rocketV1range:
            marker_lats.append(t.Pos.latitude)
            marker_lngs.append(t.Pos.longitude)
gmap.scatter(marker_lats, marker_lngs, '#2f00ff', size=200, marker=False)
for t in rockets:
    if not t.fired:
        if t.range == rocketV2range:
            marker_lats.append(t.Pos.latitude)
            marker_lngs.append(t.Pos.longitude)
gmap.scatter(marker_lats, marker_lngs, '#4593ff', size=200, marker=False)

marker_lats = []
marker_lngs = []
for t in observers:
    marker_lats.append(t.Pos.latitude)
    marker_lngs.append(t.Pos.longitude)
gmap.scatter(marker_lats, marker_lngs, '#c69aff', size=200, marker=False)

gmap.apikey = "AIzaSyCgYgSUGCBI5oxHEW-X_AXDBCj668Ei9zY"
gmap.draw("RestOwnMap.html")

                                      
print("")
print("results in browser at file://OwnUnits.html")
print("    and in browser at file://EnemyUnits.html")
print("    and in browser at file://FireMap.html")
print("    and in browser at file://RestFiMap.html")
print("    and in browser at file://RestOwnMap.html")
print("")
print("Rest veapons:", Rocket.v1counter, "Rockets V1.", Rocket.v2counter, "Rockets V2")
print("")
print(" Enemy  destroyed  left  NumHit")
print(" Helis   ", helidestroyed, "      ", (numheli-helidestroyed))
print(" Tanks   ", tankdestroyed, "      ", (numtanks-tankdestroyed))
print(" Infantry ", infdestroyed, "      ", (numinf-infdestroyed), "     ", infhit)
print(" ActArt  ", artdestroyed, "      ", (numactiveartillery-artdestroyed))
print("")
for t in artbns:
    if t.ammo <= 0:
        print("ArtBn has spent all ", ammoinartbn, "shells")
    else:
        print("ArtBn have used", (ammoinartbn - t.ammo), "155mm shells", t.ammo, "left")
print("")
for t in panserhaubits:
    if t.numgranat <= 0:
        print("PanserHaubits has spent all ", numGRA, "Guided Rocket Assisted shells")
    else:
        print("PanserHaubits has ", t.numgranat, "Guided Rocket Assisted shells left")
print("")
print("Simulation finished")
