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

Parameters = ['D','Tc_in','mfr_h']
Dictionnaries = ['geom','flowInputs','opCond']
Starts = [0.02, -10+273.15, 10]
Ends = [0.06, 10+273.15, 50]
Number_points = [2,3,4]

sim=0

for Param in Parameters:


    opCond = {}
    geom = {}
    flowInputs = {}

    # Operating Conditions
    opCond['FluidType'] = 'R134a'
    opCond['mfr_c'] = 5
    # opCond['mdot_h'] = 103.0 # Need to guess it
    opCond['TubeMat'] = 'copper'
    opCond['TubeThermalConductivity']= 400

    # Geometrical Inputs
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
    geom['corr'] = 'Cooper'
    geom['corrPD'] = 'Gaddis'
    geom['layout'] = 'InLine'
    geom['N'] = geom['Nt']*geom['Nt_col']

    # Flow Inputs
    flowInputs['Tc_in'] = 0 + 273.15
    flowInputs['Th_in'] = 15+ 273.15
    flowInputs['Ph_in'] = 1e5
    flowInputs['xc_in'] = 0.05
    Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])

    opCond['mfr_h'] = 20.0 #mfr_hGuess
    opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
    opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

    configuration = {'opCond': opCond, 'geom': geom, 'flowInputs':flowInputs}

    Dico = Dictionnaries[sim]
    configuration['filename'] = 'Resluts_parametric_'+Param+'_'+strftime("%Y-%m-%d %H-%M-%S", gmtime())+'.txt'

    start = Starts[sim]
    end = Ends[sim]
    N_points= Number_points[sim]

    variable = np.linspace(start, end, num=N_points)

    for var in variable:

        configuration[Dico][Param] = var

        f=open('./Param/'+configuration['filename'], 'a')

        f.write('\n' +Param+' = '+str(var)+'\n')
        f.close()

        simu = Simulation()

        simu.startSimulation(configuration)

    sim +=1
