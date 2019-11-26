#!/user/bin/python3
"""Global variables for Autonome Veapon Simulation
"""
# Simulation parameters
simtime = 5        # Simulation time in minutes
simrate = 1/1       # i.e. 1/60 is 1 minute simtime : 60 minutes realtime.
                    # Only speeds up target movements!

obsolete = 60     # time in sec to remove target from messages

# Targets:
numtanks  = 30              # TANKS PARAMETERS:
tanksound = 4000            # Max detection range at max speed
tankspeed = 40  # Km/h      # Max speed

numheli   =  15             # HELICOPTER PARAMETERS:
helisound = 6000            # Max detection range at max speed
helispeed = 200             # Km/h Max speed


# Observers:
numobserver = 60            # OBSERVER PARAMETERS
observervisual = 2000       # Visual detection range ( 0 for FOG :-)
                            # Sound detection based on Target sounds
# Autonome Veapons
numinf    = 15              # INFANTRY PARAMETERS (company size)
infsound  = 1200            # Max detection range at max speed
infspeed  = 5   # Km/h      # Max speed

numactiveartillery = 18     # ACTIVE ARTILLERY PARAMETERS
artsound  = 3000            # Max detection range at max speed
firesound = 7000            # Detection range when fireing
artspeed  = 40  # Km/h      # Max speed

numrocketV1 = 60            # RocketV1 PARAMETERS:
rocketV1range = 2900        # Range
V1Speed = 200   # m/s
V1hitrate = 80  # %         # Kill probabillity Rocket V1 and V2

numrocketV2 = 60            # RocketV2 PARAMETERS:
rocketV2range = 6000        # Range
V2Speed = 300               # m/s

                            # Artillery Batalions
numartbn = 1                # ARTBN PARAMETERS
artbnrange = 40000          # Range     
V0art = 800     # m/s
ammoinartbn = 1500          # Ammunition available
roundstofire = 6            # Salvos to fire
V2hitrate = 80  # %         # Kill probabillity Guided RA ammo
numbnobserver = numartbn * 16         # Regular observer teams incl.Artjeger

# PanserHaubits
numPH = 3 * numartbn        # One gun dedicated from each battery
PHrange = 40000
PHv0 = 800
PHhitrate = 80
numGRA = 20                 # Guided Rocket Assisted shots per gun
# Setting up map area

# Global List of Objets variables
messages = []
tanks = []
helis = []
artbns = []
activeartillery = []
observers = []
bnobservers = []
rockets = []
drones = []
infantry = []
panserhaubits = []
