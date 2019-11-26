#!/user/bin/python3
from numpy import random, cos
import gmplot
# Defined Classes for the simulation:
import SimAutonomVeapon5
from SimAutonomVeapon5 import Autonome, Rocket, Observer,BnObserver, ArtBn
from SimAutonomVeapon5 import PanserHaubits, gmap1
import TargetClass
from TargetClass import Tanks, Heli, Infantry, ActiveArtillery
# Contains all the parameters to change for Simulation:
import AutonomeGlobals
from AutonomeGlobals import simtime, simrate
# number of objects in simulation:
from AutonomeGlobals import numtanks, numheli, numartbn, numinf, numactiveartillery
from AutonomeGlobals import numrocketV1, numrocketV2, numobserver, rocketV1range, rocketV2range
from AutonomeGlobals import numbnobserver, bnobservers
from AutonomeGlobals import V1hitrate, V2hitrate, V1Speed, V2Speed
from AutonomeGlobals import ammoinartbn, artbnrange, V0art, observervisual
from AutonomeGlobals import numPH, PHrange, PHv0, PHhitrate, numGRA

# Object container lists:
from AutonomeGlobals import tanks, helis, observers, artbns, panserhaubits
from AutonomeGlobals import rockets, infantry, activeartillery

#import AreaDef
#from AreaDef import fromLat, fromLon

# FUTURE IMPROVEMENT IS TO MAKE AN APP TO DEFINE WAR THEATER
# AND PLACE TARGETS OBSERVERS AND UNITS ON A GEOGRAPHIC MAP.
# IN THE MEANTIME WE MAKE A SQUARE AND PLACE ALL AT RANDOM


# Generate Targets, and Autonome veapons and place randomly
def generatewarmap(lat, lon, height, width):
    fromLat = lat
    fromLon = lon
    hA = height/1.11/100
    wA = width/1.11/100/cos(fromLat/360*6.28)   
    # Make string and set parameters below

    # Make map for WEB
    gmap = gmplot.GoogleMapPlotter(fromLat+hA/2, fromLon+wA/2, 12) # zoom level last
    
    # All enemy:
    lat_list = []
    lon_list = []   
    for t in range(0, numinf):
        t = Infantry(str(random.uniform(fromLat,fromLat+hA))+" "+str(random.uniform(fromLon,fromLon+wA)))
        infantry.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.heatmap( lat_list, lon_list )    # One way to do it, the other used below
    
    lat_list = []
    lon_list = []   
    for t in range(0,numactiveartillery):
        t = ActiveArtillery(str(random.uniform(fromLat,fromLat+hA))+" "+str(random.uniform(fromLon,fromLon+wA)))
        activeartillery.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#fff400', size=200, marker=False) 

    lat_list = []
    lon_list = []   
    for t in range(0,numtanks):
        t = Tanks(str(random.uniform(fromLat,fromLat+hA))+" "+str(random.uniform(fromLon,fromLon+wA)))
        tanks.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
        gmap.scatter(lat_list, lon_list, '#ff0000', size=200, marker=False) 

    lat_list = []
    lon_list = []   
    for t in range(0,numheli):
        t = Heli(str(random.uniform(fromLat,fromLat+hA))+" "+str(random.uniform(fromLon,fromLon+wA)))
        helis.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#ff7b00', size=200, marker=False)
    
    gmap.apikey = "AIzaSyCgYgSUGCBI5oxHEW-X_AXDBCj668Ei9zY"  
    gmap.draw( "EnemyUnits.html")
    
    # All Own unit
    gmap = gmplot.GoogleMapPlotter(fromLat+hA/2, fromLon+wA/2, 12) # zoom level last
    
    lat_list = []
    lon_list = []   
    for t in range(0, numobserver):
        t = Observer(str(random.uniform(fromLat,fromLat+hA))+
                 " "+str(random.uniform(fromLon,fromLon+wA)), observervisual)
        observers.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#c69aff', size=200, marker=False)
#        gmap.marker( t.Pos.latitude, t.Pos.longitude, 'violet' )

    lat_list = []
    lon_list = []   
    for t in range(0, numrocketV1):
        t = Rocket(str(random.uniform(fromLat,fromLat+hA))+
                 " "+str(random.uniform(fromLon,fromLon+wA))
                         ,rocketV1range, V1Speed, V1hitrate)
        rockets.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#2f00ff', size=200, marker=False)       

    lat_list = []
    lon_list = []   
    for t in range(0, numrocketV2):
        t = Rocket(str(random.uniform(fromLat,fromLat+hA))+
                 " "+str(random.uniform(fromLon,fromLon+wA))
                         ,rocketV2range, V2Speed, V2hitrate)
        rockets.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#4593ff', size=200, marker=False)       

# ArtBn
    lat_list = []
    lon_list = []   
    for t in range(0, numPH):
        t = PanserHaubits(str(random.uniform(fromLat-0.03,fromLat-0.05))+
                 " "+str(random.uniform(fromLon,fromLon+wA))
                        ,PHrange, PHv0, PHhitrate, numGRA)
        panserhaubits.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#00ff04', size=200, marker=False)             
#        gmap.marker( t.Pos.latitude, t.Pos.longitude, 'green' )
    lat_list = []
    lon_list = []
    for t in range(0, numartbn*4): #Place ArtJegers
        t = BnObserver(str(random.uniform(fromLat,fromLat+hA))+
                 " "+str(random.uniform(fromLon,fromLon+wA)), observervisual)
        bnobservers.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#ff8acb', size=200, marker=False)                    
#        gmap.marker( t.Pos.latitude, t.Pos.longitude, 'pink' )
    lat_list = []
    lon_list = []
    for t in range(numartbn*4, numartbn*16): #Place Observation teams
        t = BnObserver(str(random.uniform(fromLat,fromLat+0.03))+
                 " "+str(random.uniform(fromLon,fromLon+wA)), observervisual)
        bnobservers.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#ff8acb', size=200, marker=False)                            
#       gmap.marker( t.Pos.latitude, t.Pos.longitude, 'pink' )
    lat_list = []
    lon_list = []
    for t in range(0, numartbn):  # Place in corner :-)
        t = ArtBn(str(random.uniform(fromLat-0.03,fromLat-0.05))+
                 " "+str(random.uniform(fromLon,fromLon+wA))
            , artbnrange, V0art, V2hitrate)
        artbns.append(t)
        lat_list.append(t.Pos.latitude)
        lon_list.append(t.Pos.longitude)
    gmap.scatter(lat_list, lon_list, '#ff8acb', size=400, marker=False)                       
#        gmap.marker( t.Pos.latitude, t.Pos.longitude, 'blue' )

    gmap.apikey = "AIzaSyCgYgSUGCBI5oxHEW-X_AXDBCj668Ei9zY"  
    gmap.draw( "OwnUnits.html")

    print("You   may see own units on Map at file://01Python/AutonomeVeapons/OwnUnits.html")
    print("You may see enemy units on Map at file://01Python/AutonomeVeapons/EnemyUnits.html")
    input("Press <Enter> to start simulation. ")
###
