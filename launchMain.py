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
<<<<<<< HEAD
opCond['FluidType'] = 'R134a'
opCond['mfr_c'] = 5
=======
opCond['FluidType'] = 'Propane'
opCond['mfr_c'] = 8
>>>>>>> PlotsPresentation

# opCond['mdot_h'] = 103.0 # Need to guess it
opCond['TubeMat'] = 'Copper'
opCond['TubeThermalConductivity']= 400

# Geometrical Inputs
<<<<<<< HEAD
geom['Nt'] = 10
geom['Nt_col'] = 5
geom['L'] = 5
geom['n'] = 3
geom['s'] = 70e-3
geom['sh'] = 70e-3
geom['D'] = 50e-3
geom['e_i'] =3e-6
geom['e_o'] = 3e-6
geom['t'] = 5e-3

=======

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
>>>>>>> PlotsPresentation
geom['corr'] = 'Cooper'
geom['corrPD'] = 'Gaddis'
geom['layout'] = 'InLine'
geom['N'] = geom['Nt']*geom['Nt_col']

# Flow Inputs
<<<<<<< HEAD
flowInputs['Tc_in'] = 0 + 273.15
flowInputs['Th_in'] = 15+ 273.15

=======
flowInputs['Tc_in'] = 5 + 273.15
flowInputs['Th_in'] = 25+ 273.15
>>>>>>> PlotsPresentation
flowInputs['Ph_in'] = 1e5
flowInputs['xc_in'] = 0.2
Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])

opCond['mfr_h'] = 1 #mfr_hGuess [kg/s]
opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2) #[kg/m^2s]
#opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])
opCond['mdot_c'] = 10.0 #[kg/m^2s]

<<<<<<< HEAD
#print(opCond['mdot_h'])
=======
opCond['mfr_h'] = 30.0 #mfr_hGuess
opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

print(opCond['mdot_h'])
>>>>>>> PlotsPresentation


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

try:
    simu.startSimulation(configuration)

except Error as e:
    if e.functionName == 'q_dnb':
        print(e.message)
    else:
        print('\n An unexpected error has occured, check inputs \n \n \n \n \n or just stop messing with our code Jackson')

except Exception as e:

    print('\n An unexpected error has occured, check inputs \n \n \n \n \n or just stop messing with our code Jackson')
