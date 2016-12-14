import sys
import math
import numpy as np

from properties import get_properties
from CoolProp.CoolProp import PropsSI

from feenstraCorrelation import ini_cell_voidFraction
from SolveCell import SolveCell
from Postprocess import plot_boiler
from Postprocess import plot_xc_pipe

from PyQt5.QtCore import QObject, pyqtSignal

from mainSimulation import Simulation

from time import gmtime, strftime


################################################################################
###                     EDIT BASE CONFIGURATION HERE                         ###

opCond = {}
geom = {}
flowInputs = {}

# Operating Conditions
opCond['FluidType'] = 'R134a'
#opCond['mfr_c'] = #[kg/s]
# opCond['mdot_h'] = 103.0 # Need to guess it
opCond['TubeMat'] = 'Copper'
opCond['TubeThermalConductivity']= 400

# Geometrical Inputs
geom['Nt'] = 8
geom['Nt_col'] = 2
geom['L'] = 1.027
geom['n'] = 10
geom['s'] = 22.22e-3
geom['sh'] = 22.22e-3
geom['D'] = 18.87e-3
geom['e_i'] =2.3e-6
geom['e_o'] = 2.3e-6
geom['t'] = 2.28e-3
geom['corr'] = 'Cooper'
geom['corrPD'] = 'Gaddis'
geom['layout'] = 'Staggered'
geom['N'] = geom['Nt']*geom['Nt_col']

# Flow Inputs
flowInputs['Tc_in'] = 15 + 273.15
flowInputs['Th_in'] = 20+ 273.15
flowInputs['Ph_in'] = 1e5
flowInputs['xc_in'] = 0.2
Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])

opCond['mfr_h'] = 0.5 #mfr_hGuess [kg/s]
opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2) #[kg/m^2s]
#opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])
opCond['mdot_c'] = 10.0 #[kg/m^2s]


configuration = {'opCond': opCond, 'geom': geom, 'flowInputs':flowInputs}


Param = 'D'
Dico = 'geom'

start = 20e-3
end = 60e-3
N_points=2

variable = np.linspace(start, end, num=N_points)

for var in variable:

    configuration[Dico][Param] = var

    f=open('./Param/Results_Parametric.txt', 'a')

    f.write('\n' +Param+' = '+str(var)+'\n Time: '+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    f.close()

    simu = Simulation()

    simu.startSimulation(configuration)
