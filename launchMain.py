import sys
import math
import numpy as np

from properties import get_properties
from CoolProp.CoolProp import PropsSI

from feenstraCorrelation import ini_cell_voidFraction
from SolveCell import SolveCell
from mdothDesired import guessMassFlow
from Postprocess import *

from PyQt5.QtCore import QObject, pyqtSignal

from mainSimulation import Simulation
opCond = {}
geom = {}
flowInputs = {}

# Operating Conditions
opCond['FluidType'] = 'R134a'
opCond['mfr_c'] = 2
# opCond['mdot_h'] = 103.0 # Need to guess it
opCond['TubeMat'] = 'copper'
opCond['TubeThermalConductivity']= 400

# Geometrical Inputs
geom['Nt'] = 4
geom['Nt_col'] = 6
geom['L'] = 3.0
geom['n'] = 7
geom['s'] = 150e-3
geom['sh'] = 150e-3
geom['D'] = 100e-3
geom['e_i'] =3e-6
geom['e_o'] = 3e-6
geom['t'] = 10e-3
geom['corr'] = 'Cooper'
geom['corrPD'] = 'Gaddis'
geom['layout'] = 'Staggered'
geom['N'] = geom['Nt']*geom['Nt_col']


# Flow Inputs
flowInputs['Tc_in'] = 0 + 273.15
flowInputs['Th_in'] = 25+ 273.15
flowInputs['Ph_in'] = 1e5
flowInputs['xc_in'] = 0.05
Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])


opCond['mfr_h'] = 15 #mfr_hGuess
opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

print(opCond['mdot_h'])

configuration = {'opCond': opCond, 'geom': geom, 'flowInputs':flowInputs}

simu = Simulation()
simu.startSimulation(configuration)