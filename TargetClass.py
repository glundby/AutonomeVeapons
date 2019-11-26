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
from random import randint
from geopy.point import Point

import threading

from AutonomeGlobals import simtime, simrate
from AutonomeGlobals import tanksound, tankspeed, helisound, helispeed
from AutonomeGlobals import infsound, infspeed, artsound, artspeed, firesound


class Vehicle(threading.Thread):
    """Generic vehicle for simulating! (subclass of Thread)
       Not meant to be instantiated as objects"""
    vcount = 0         # example of Global counter for class
    Lock = threading.Lock()  # Global threading.Lock for class
    # global simtime
    # global messages
    
    def __init__(self, posisjon):  # Run only once for new object
        threading.Thread.__init__(self)  # Makes new object a .Thread
        self.Pos = Point(posisjon)
        Vehicle.vcount += 1    # Increment Global Vehicles counter 
        self.speed = 0
                               # Init vehicle in random direction
        self.direction = np.random.randint(0, 360)
        self.last = time()     # Starting simulation clock
                         
    def run(self):             # called by the super class threading.Thread.start()
        Vehicle._activity(self)  # The main running part of the object!

    def exit(self):            # call to the super class threading ???
        pass           

    def _move(self):  # Calculates simulation values
        # speed = self.speed          # Local variables !!! Hva gjør denne?
        # direction = self.direction  # set by object globals
        # if self.speed == 0:         # Protect against div by zero
        #    pass                    # Don't move
        # else:

        speed = self.speed * 1000 / 3600    # Convert to m/s
        direction = np.deg2rad(self.direction)   # Convert to rad
        deltatime = time() - self.last  # Find time passed!
        self.last = time()              # For next time.
        s = speed * deltatime / simrate         # Driven since last.
        dx = np.sin(direction) * s      # Delta x and delta y
        dy = np.cos(direction) * s      # 1 m earth surface in radians
        self.Pos.longitude = self.Pos.longitude + np.rad2deg(dx * 2.49938265248e-8)  # 1/earth circ
        self.Pos.latitude = self.Pos.latitude + np.rad2deg(dy * 2.49938265248e-8)
            
    def _activity(self):
        counter = simtime * 60       # in seconds
        while counter > 0:           # Number of SIM steps left
            dtime = np.random.randint(10, 20)  # next driving time
            counter -= dtime
            sleep(dtime)
            # Drive in random direction (no U-turn) with random speed!
            self.direction = self.direction + np.random.randint(-90, 90)
            if self.direction < 0:
                self.direction = self.direction + 360
            elif self.direction > 360:
                self.direction = self.direction - 360
            self.speed = np.random.randint(0, self.maxspeed)
            if type(self).__name__ == "ActiveArtillery":
                if self.fireing:
                    self.fireing = False  # Alternate between fireing
                    self.sounrange = artsound * self.speed / self.maxspeed
                else:                    # not fireing
                    self.fireing = True
                    self.soundrange = firesound
            else:
                self.soundrange = self.maxsound * self.speed / self.maxspeed
            if type(self).__name__ == "Tanks":
                if self.speed < 10:
                    self.fireing = True  # Slowing to fireing
                    self.sounrange = firesound
                else:                    # not fireing
                    self.fireing = False
                    self.soundrange = tanksound * self.speed / self.maxspeed
            else:
                self.soundrange = self.maxsound * self.speed / self.maxspeed
            if self.destroyed:
                self.speed = 0
                return    # Retire object from simulation
            
            self._move()  # Calculate new position.
        # end while


# So then we can start defining subclasses of Vehicle inheriting all the attributes and methods
# and we can add new attributes as we wish.....

class Tanks(Vehicle):            # Subclass of Vehicle inherits all
    """Generic Tanks  attributes and methods from Vehicle"""

    counter = 0                # Own Class Car counter

    def __init__(self, Pos):  
        super().__init__(Pos)  # Uses superclass __init__!!!
        self.maxspeed = tankspeed
        self.maxsound = tanksound
        self.soundrange = 0
        Tanks.counter += 1        # Counts up one more Tank
        self.detected = False     # Detected by one or more Observers and fixed pos
        self.destroyed = False
        self.designated = False
        self.fireing = False


class Heli(Vehicle):            # Subclass of Vehicle inherits all
    """Generic Heli. Attributes and methods from Vehicle."""

    counter = 0                # Own Class Buss counter

    def __init__(self, Pos):
        super().__init__(Pos)  # Uses superclass __init__!!!
        self.maxspeed = helispeed
        self.maxsound = helisound
        self.soundrange = 0
        Heli.counter += 1        # Counts up one more Helicopter
        self.detected = False
        self.destroyed = False
        self.designated = False
        self.fireing = False


class Infantry(Vehicle):
    """Generic Infantry platoon on foot. When driving they are Tanks."""

    counter = 0

    def __init__(self, Pos):
        super().__init__(Pos)
        self.maxspeed = infspeed
        self.maxsound = infsound
        self.soundrange = 0
        Infantry.counter += 1
        self.detected = False
        self.destroyed = False
        self.designated = False
        self.strength = 100     # % at start of simulation
                                # looses 10% per salvo from ArtBn
        self.fireing = False


class ActiveArtillery(Vehicle):
    """Generic Artillery unit. """

    counter = 0

    def __init__(self, Pos):
        super().__init__(Pos)
        self.maxspeed   = artspeed
        self.maxsound   = artsound
        ActiveArtillery.counter += 1
        self.detected = False
        self.destroyed = False
        self.designated = False
        if randint(1, 2) == 1:
            self.fireing = False
            self.soundrange = artsound
        else:
            self.fireing = True
            self.soundrange = firesound

            
# May add more sub classes here with extra attributes, parameters and
# methods as needed.... May also override superclass Vehicle
