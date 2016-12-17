import sys
import math
import numpy as np

from CoolProp.CoolProp import PropsSI

from feenstraCorrelation import ini_cell_voidFraction
from SolveCell import SolveCell
from Postprocess import plot_boiler
from Postprocess import plot_xc_pipe

from PyQt5.QtCore import QObject, pyqtSignal

from mainSimulation import Simulation


opCond = {}
geom = {}
flowInputs = {}

# Operating Conditions
opCond['FluidType'] = 'Propane'
opCond['mfr_c'] = 8

# opCond['mdot_h'] = 103.0 # Need to guess it
opCond['TubeMat'] = 'copper'
opCond['TubeThermalConductivity']= 400

# Geometrical Inputs

geom['Nt'] = 11
geom['Nt_col'] = 11
geom['L'] = 3.0
geom['n'] = 15
geom['s'] = 45e-3
geom['sh'] = 45e-3
geom['D'] = 30e-3
geom['e_i'] =200e-6
geom['e_o'] = 200e-6
geom['t'] = 3e-3
geom['corr'] = 'Cooper'
geom['corrPD'] = 'Gaddis'
geom['layout'] = 'Staggered'
geom['N'] = geom['Nt']*geom['Nt_col']


# Flow Inputs
flowInputs['Tc_in'] = 5 + 273.15
flowInputs['Th_in'] = 25+ 273.15
flowInputs['Ph_in'] = 1e5
flowInputs['xc_in'] = 0.05
Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])


opCond['mfr_h'] = 30.0 #mfr_hGuess
opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

print(opCond['mdot_h'])


'''
#### Initialization ####
'''
np.set_printoptions(precision=2)
# Matrix allocation for every thermodynamical variable
Th = np.matrix([[0.0 for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )
Tc = np.matrix([[0.0 for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )
Ph = np.matrix([[1e5 for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )
Pc = np.matrix([[1e5 for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )
eps = np.matrix([[0.0 for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )
xc = np.matrix([[0.0 for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )
OtherData = np.matrix([[{} for x in range(geom['n'] + 1)] for y in range(geom['Nt'] + 1)] )


# Initialization of the first row and column
# Non-used cells in the matrix are set with '-1'
Tc[0,:] = flowInputs['Tc_in']
Tc[:,0] = -1
Th[:,0] = flowInputs['Th_in']
Th[0,:] = -1

Pc[0,:] = Pc_in
Pc[:,0] = -1
Ph[:,0] = flowInputs['Ph_in']
Ph[0,:] = -1

xc[0,:] = flowInputs['xc_in']
xc[:,0] = -1


epsInit = ini_cell_voidFraction(opCond, geom, flowInputs['xc_in'], flowInputs['Tc_in'], 0.5)
eps[0,:] = epsInit
eps[:,0] = -1
configuration = {'opCond': opCond, 'geom': geom, 'flowInputs':flowInputs}

simu = Simulation()
simu.startSimulation(configuration)
