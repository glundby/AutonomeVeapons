#!/user/bin/python3
"""
TEST OF OBJECT ORIENTED "CONCURRENT" SIMULATION         
Defining superclass Vehicle(treading.Tread) for
multitreading "concurrent" execution and simulation.
Generating several subclass(Vehicle) to test.
"""
import time
from time import time
from time import sleep
import numpy as np
from numpy import random
from random import randint
from math import sqrt
from geopy.point import Point
import threading
from AutonomeGlobals import simtime, messages, obsolete
from AutonomeGlobals import tanks, helis, infantry, activeartillery
from AutonomeGlobals import ammoinartbn, roundstofire

from AreaDef import gmap1


class Autonome(threading.Thread):
    """Generic vehicle for simulating! (subclass of Thread)
       Not meant to be instantiated as objects"""
    
    Lock = threading.Lock()  # Global threading.Lock for class
    MessageLock = threading.Lock()
   
    def __init__(self, posisjon):  # Run only once for new object
        threading.Thread.__init__(self)  # Makes new object a .Thread
        self.Pos = Point(posisjon)
        self.last = time()     # Starting simulation clock
        self.oldt = time()
        self.timestamp = time()

    # noinspection PyUnresolvedReferences
    def run(self):              # called by the super class threading.Thread.start()
                                # The main running part of the object!        
        self._activity()

    # noinspection PyMethodMayBeStatic
    def g2(self):  # Removes obsolete targets allowing them to be observed again
        now = time()
        Autonome.MessageLock.acquire()        # Reserve messages during cleanup
        for t in messages:
            if type(t).__name__ == "Heli":
                toold = obsolete / 4
            elif type(t).__name__ == "Infantry":
                toold = obsolete * 4
            else:
                toold = obsolete     
            if (now - t.timestamp) >= toold:    # when obsolete take out of messages
                t.detected = False                 # re designate object possibly in
                t.designated = False               # new position after it has moved
                t.timestamp = time()               # in case we need to know when in messages
                if not messages == []:
                    messages.pop(messages.index(t))
        Autonome.MessageLock.release()        # Free messages for others
                 
# So then we can start defining subclasses of Autonome inheriting all the attributes and methods
# and we can add new attributes as we wish.....


class Observer(Autonome):
    """Generic stationary Observer' # Subclass of Autonome inherits all attributes and methods from Autonome."""

    counter = 0

    def __init__(self, posisjon, visibility):  # Own Class Observer counter
        super().__init__(posisjon)  # Uses Superclass __init__!!"
        self.maxspeed = 0         
        Observer.counter += 1
        self.visualrange = visibility
        self.fireunits = []       # Easier to work on a concatenated list since same treatment Observer
        self.fireunits.extend(activeartillery)
        self.fireunits.extend(tanks)
        self.fireunits.extend(helis)
        self.fireunits.extend(infantry)
        random.shuffle(self.fireunits)      # Make treatment happen in random sequence
        
    def _activity(self):
        counter = simtime * 60              # in seconds
        while counter > 0:                  # SIM time left
            spendtime = np.random.randint(1, 5)  # spend some sim time and wake up
            counter -= spendtime       
            sleep(spendtime)          

            for t in self.fireunits:
                if counter <= 0:
                    break
                if not t.destroyed:
                    if not t.designated:
                        dlon = t.Pos.longitude - self.Pos.longitude
                        dlat = t.Pos.latitude - self.Pos.latitude      
                        rdist = sqrt(dlon**2 + dlat**2)
                        vincinity = rdist * 60 * 1842.905  # minutes to m on earth surface
                        if vincinity < self.visualrange:
                            spendtime = np.random.randint(1, 5)  # time to do target
                            counter -= spendtime
                            sleep(spendtime)
                            t.timestamp = time()
                            messages.append(t)
                            t.designated = True
                            t.detected = True
                            Autonome.Lock.acquire()
                            print("Observer visually Designated ", type(t).__name__, t.Pos)
                            gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                       (self.Pos.longitude, t.Pos.longitude),
                                       'lightblue', edge_width=3.0)
                            Autonome.Lock.release()
                        elif vincinity < t.soundrange:  # Noise when fireing is loud
                            spendtime = np.random.randint(1, 5)  # time to do target
                            counter -= spendtime      # 
                            sleep(spendtime)          #
                            if t.detected:
                                t.designated = True
                                if t.fireing:
                                    Autonome.Lock.acquire()
                                    print("Observer Designated fireing ", type(t).__name__, t.Pos)
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'indigo', edge_width=3.0)
                                    Autonome.Lock.release()
                                else:
                                    Autonome.Lock.acquire()
                                    print("Observer Designated ", type(t).__name__, t.Pos)
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'black', edge_width=2.0)
                                    Autonome.Lock.release()
                            else:
                                t.detected = True
                                Autonome.Lock.acquire()
                                print("Observer Detected New ", type(t).__name__)
                                gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                           (self.Pos.longitude, t.Pos.longitude),
                                           'lightgreen', edge_width=3.0)
                                Autonome.Lock.release()
                            t.timestamp = time()
                            messages.append(t)


class BnObserver(Observer):

    def __init__(self, posisjon, visibility):  # Own Class Observer counter
        super().__init__(posisjon, visibility)  # Uses Superclass __init__!!"

    def _activity(self):        # Override Super activity
        counter = simtime * 60            # in seconds
        while counter > 0:                # SIM time left
            spendtime = np.random.randint(5, 15)  # spend some sim time and wake up
            counter -= spendtime
            sleep(spendtime)

            for t in self.fireunits:
                if counter <= 0:
                    break
                if not t.destroyed:
                    if not t.designated:
                        dlon = t.Pos.longitude - self.Pos.longitude
                        dlat = t.Pos.latitude - self.Pos.latitude      
                        rdist = sqrt(dlon**2 + dlat**2)
                        vincinity = rdist * 60 * 1842.905  # minutes to m on earth surface
                        if vincinity < self.visualrange:
                            spendtime = np.random.randint(1, 5)  # time to do target
                            counter -= spendtime
                            sleep(spendtime)
                            t.timestamp = time()
                            messages.append(t)
                            t.designated = True
                            t.detected = True
                            Autonome.Lock.acquire()
                            print("BnObserver visually Designated ", type(t).__name__, t.Pos)
                            gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                       (self.Pos.longitude, t.Pos.longitude),
                                       'pink', edge_width=3.0)
                            Autonome.Lock.release()
                # No sound based detection

    
class Rocket(Autonome):          # Subclass of Autonome inherits all
    """Generic Short and long distance Rocket. attributes and methods from Autonome."""
    v1counter = 0
    v2counter = 0   # Own Class Rocket counter

    def __init__(self, posisjon, maxrange, maxspeed, hitrate):
        super().__init__(posisjon)  # Uses superclass __init__!!!
        self.maxspeed = maxspeed    # flight speed
        self.range = maxrange       # Practical range
        self.hitrate = hitrate
        if self.range < 3000:
            Rocket.v1counter += 1       # Counts up one more Rocket
        else:
            Rocket.v2counter += 1
        self.fired = False
        
    def _activity(self):                    # Stationary objects
        counter = simtime * 60              # in seconds
        while counter > 0:                  # SIM time left
            if self.range < 3000:           # V1 rocket pri 1
                spendtime = 1
            else:
                spendtime = 3               # V2 rocket pri 2   
            counter -= spendtime            # Slow down simulation
            sleep(spendtime)                # needed to let cpu breath
            # self.G2()                     # remove old target from messages
                
            for t in reversed(messages):
                if counter <= 0:
                    break
                if not (type(t).__name__ == "Infantry"):
                    if t.designated and (not t.destroyed):
                        dlon = t.Pos.longitude - self.Pos.longitude
                        dlat = t.Pos.latitude - self.Pos.latitude
                        rdist = sqrt(dlon**2 + dlat**2)
                        vincinity = rdist * 60 * 1842.905  # 1 min = 1843m
                        if vincinity < self.range:
                            t.destroyed = True  # Flag to reserve target avoid double kill
                            flight = vincinity / self.maxspeed  # Time of flight
                            sleep(int(flight))
                            counter -= flight
                            if randint(0, 100) < self.hitrate:
                                t.destroyed = True
                                t.counter = t.counter - 1
                                Autonome.Lock.acquire()
                                print("            ", type(self).__name__, "Destroyed Target", type(t).__name__)
                                if type(t).__name__ == "Heli":
                                    gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'orange')
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'orange', edge_width=3.0)
                                elif type(t).__name__ == "ActiveArtillery":
                                    gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'yellow')
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'yellow', edge_width=3.0)
                                else:
                                    gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'red')
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'red', edge_width=3.0)
                                Autonome.Lock.release()
                            else:
                                t.destroyed = False  # Did not get it!
                                t.detected = False
                                t.designated = False
                            if self.range < 3000:
                                Rocket.v1counter -= 1
                            else:
                                Rocket.v2counter -= 1
                            self.fired = True
                            return  # Terminate process, No reuse of rockets


class ArtBn(Autonome):             # Subclass of Autonome inherits all
    """Generic ArtBn'          # attributes and methods from Autonome."""

    counter = 0                    # Own Class ArtBn counter

    def __init__(self, posisjon, maxrange, maxspeed, hitrate):
        super().__init__(posisjon)  # Uses superclass __init__!!!
        self.maxspeed = maxspeed    # Flight speed
        self.range = maxrange       # Practical range
        self.hitrate = hitrate      # Hitrate used for Guided RocketAsisted munition
        ArtBn.counter += 1           # Counts up one more ArtBn
        self.ammo = ammoinartbn     # Avd amm

    def _activity(self):                    # Stationary objects
        counter = simtime * 60              # in seconds
        while counter > 0:                  # SIM time left
            spendtime = 1
            counter -= spendtime      # Slow down simulation
            sleep(spendtime)          # needed to let cpu breath

            self.g2()         # remove old targets from messages

            for t in reversed(messages):
                if counter <= 0:
                    break
                if type(t).__name__ == "Infantry":
                    if t.designated and (not t.destroyed):
                        dlon = t.Pos.longitude - self.Pos.longitude
                        dlat = t.Pos.latitude - self.Pos.latitude
                        rdist = sqrt(dlon**2 + dlat**2)
                        vincinity = rdist * 60 * 1842.905  # 1 min = 1843m
                        if vincinity < self.range:
                            # sleep( vincinity / self.maxspeed ) #Time of flight
                            t.destroyed = True  # Flag to reserve target
                            sleep(20*roundstofire)       # Time for each round
                            counter -= 20*roundstofire   # Spending simulation time
                            t.strength = t.strength - 10*roundstofire  # % reduction
                            Autonome.Lock.acquire()
                            print("             ArtBn fired ", 15*roundstofire, "shells at Target", type(t).__name__)
                            Autonome.Lock.release()
                            self.ammo = self.ammo - 15*roundstofire
                            if t.strength <= 50:
                                Autonome.Lock.acquire()
                                gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'white')
                                print("             ArtBn DESTROYED ", type(t).__name__)
                                gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                           (self.Pos.longitude, t.Pos.longitude),
                                           'white', edge_width=3.0)
                                Autonome.Lock.release()
                                t.destroyed = True           
                            else:
                                gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'gray')
                                gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                           (self.Pos.longitude, t.Pos.longitude),
                                           'gray', edge_width=3.0)
                                t.destroyed = False     # Use flag to avoid double fire
                                t.detected = False      # Release for new detection
                                t.designated = False    # and new designation ( have moved away )
                if self.ammo <= 0:
                    Autonome.Lock.acquire()
                    print("*****************ArtBn EMPTY!*******************")
                    Autonome.Lock.release()
                    return
                    # nothing more to do in simulation for this ArtBn
                    
            # End for t in messages


class PanserHaubits(Autonome):          # Subclass of Autonome inherits all
    """Dedicated Atillery gun with Guided Rocket Assisted ammo ' # attributtes and methods from Autonome"""

    counter = 0                    # Own Class Rocket counter

    def __init__(self, posisjon, maxrange, maxspeed, hitrate, numGRA):
        super().__init__(posisjon)  # Uses superclass __init__!!!
        self.maxspeed = maxspeed   # flight speed
        self.range = maxrange      # Practical range
        self.hitrate = hitrate
        self.numgranat = numGRA
        PanserHaubits.counter += 1       # Counts up one more PanserHaubits
        
    def _activity(self):                    # Stationary objects
        counter = simtime * 60              # in seconds
        while counter > 0:                # SIM time left
            spendtime = 1                   
            counter -= spendtime      # Slow down simulation
            sleep(spendtime)          # needed to let cpu breath
                
            for t in reversed(messages):
                if counter <= 0:
                    break
                if not ((type(t).__name__ == "Infantry") or (type(t).__name__ == "Heli")):
                    if t.designated and (not t.destroyed):
                        dlon = t.Pos.longitude - self.Pos.longitude
                        dlat = t.Pos.latitude - self.Pos.latitude
                        rdist = sqrt(dlon**2 + dlat**2)
                        vincinity = rdist * 60 * 1842.905  # 1 min = 1843m
                        if vincinity < self.range:
                            t.destroyed = True  # Flag to reserve target avoid double kill
                            # flight = vincinity / self.maxspeed # Time of flight
                            # sleep(int(flight))
                            sleep(20)         # Time per round
                            counter -= 20
                            if randint(0, 100) < self.hitrate:
                                t.counter = t.counter - 1
                                Autonome.Lock.acquire()
                                print("            ", type(self).__name__, "Destroyed Target", type(t).__name__)
                                gmap1.marker(self.Pos.latitude, self.Pos.longitude, 'green')
                                if type(t).__name__ == "ActiveArtillery":
                                    gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'yellow')
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'yellow', edge_width=3.0)
                                else:
                                    gmap1.marker(t.Pos.latitude, t.Pos.longitude, 'red')
                                    gmap1.plot((self.Pos.latitude, t.Pos.latitude),
                                               (self.Pos.longitude, t.Pos.longitude),
                                               'red', edge_width=3.0)
                                Autonome.Lock.release()
                            else:
                                t.destroyed = False  # Did not get it!
                                t.detected = False
                                t.designated = False

                            self.numgranat -= 1
                            if self.numgranat <= 0:
                                return      # Nothing more to do for this gun

# May add more sub classes here with extra attributes, parameters and
# methods as needed.... May also override superclass Vehicle
