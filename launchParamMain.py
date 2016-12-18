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

import os

###########################################################################
###                   CHOOSE PARAEMETRIC RANGES                        ###

geomKeys = ['Nt', 'Nt_col', 'L', 'n', 's', 'sh', 'D', 'e_i', 'e_o', 't', 'corr',\
    'corrPD' ,'layout', 'N']
flowInputsKeys = ['Tc_in', 'Th_in','Ph_in', 'xc_in']
opCondKeys = ['FluidType', 'TubeMat', 'TubeThermalConductivity', 'mdot_c', 'mdot_h', 'mfr_h', 'mfr_c']



# parameters 1 go on the x-axis
Parameters_1 = ['Tc_in']
Starts_1 = [-2 + 273.15]
Ends_1 = [10 + 273.15]
Number_points_1 = [13]
Parameters_names_1 = ['T_{sat}']
# what you want written as xlabel in matlab, must NOT contain spcce
# the latex interpreter is used
Dictionnaries_1 = []
for key in Parameters_1:
    if key in geomKeys:
        Dictionnaries_1.append('geom')
    elif key in opCondKeys:
        Dictionnaries_1.append('opCond')
    elif key in flowInputsKeys:
        Dictionnaries_1.append('flowInputs')
    else:
        raise Exception('Key parameters 1 is not in any dictionnaries')

# parameters 2 go in the legend
Parameters_2 = ['mdot_c']

Starts_2 = [5]
Ends_2 = [15]
Number_points_2 = [3]
Parameters_names_2 = ['G_{R134a}[kg/s/m^2]']

Dictionnaries_2 = []
for key in Parameters_2:
    if key in geomKeys:
        Dictionnaries_2.append('geom')
    elif key in opCondKeys:
        Dictionnaries_2.append('opCond')
    elif key in flowInputsKeys:
        Dictionnaries_2.append('flowInputs')
    else:
        raise Exception('Key parameters 2 is not in any dictionnaries')

sim_1 = 0
sim_2 = 0

path='./Param/'+'Parametric_analysis'+'_'+strftime("%Y-%m-%d %H-%M-%S")
os.makedirs(path)

configuration={}

for Param_2 in Parameters_2:

    configuration['filename'] = path+'/'+Param_2+'_res.txt'

    for Param_1 in Parameters_1:

################################################################################
###                     EDIT BASE CONFIGURATION HERE                         ###

        opCond = {}
        geom = {}
        flowInputs = {}

        # Operating Conditions
        opCond['FluidType'] = 'R134a'
        # opCond['mfr_c'] = 25
        # opCond['mdot_h'] = 103.0 # Need to guess it
        opCond['TubeMat'] = 'copper'
        opCond['TubeThermalConductivity']= 400

        # Geometrical Inputs
        geom['Nt'] = 8
        geom['Nt_col'] = 4
        geom['L'] = 3
        geom['n'] = 10
        geom['s'] = 22.22e-3
        geom['sh'] = 22.22e-3
        geom['D'] = 15e-3
        geom['e_i'] = 3e-6
        geom['e_o'] = 2.3e-6
        geom['t'] = 2e-3
        geom['corr'] = 'Cooper'
        geom['corrPD'] = 'Gaddis'
        geom['layout'] = 'Staggered'
        geom['N'] = geom['Nt']*geom['Nt_col']

        # Flow Inputs
        flowInputs['Tc_in'] = 0 + 273.15
        flowInputs['Th_in'] = 20 + 273.15
        flowInputs['Ph_in'] = 1e5
        flowInputs['xc_in'] = 0.05
        Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])

        #opCond['mfr_h'] = 0.5 #mfr_hGuess
        #opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
        #opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

        opCond['mdot_c'] = 5
        opCond['mdot_h'] = 300

        configuration['opCond'] = opCond
        configuration['geom'] = geom
        configuration['flowInputs'] = flowInputs

        if sim_1 == 0 & sim_2 ==0: #if it is the first simulation, we save the base configuration
            f=open(path+'/BaseConfiguration.txt','w')
            f.write(str(configuration))
            f.close()


        Dico_1 = Dictionnaries_1[sim_1]
        start_1 = Starts_1[sim_1]
        end_1 = Ends_1[sim_1]
        N_points_1 = Number_points_1[sim_1]

        variable_1 = np.linspace(start_1, end_1, num=N_points_1)

        if Param_2 == 'FluidType':
            variable_2 = ['R134a','Ammonia','Propane']
        elif Param_2 == 'corrPD':
            variable_2 = ['Gaddis','Zukauskas']
        elif Param_2 == 'layout':
            variable_2 = ['Staggered','InLine']
        else:
            start_2 = Starts_2[sim_2]
            end_2 = Ends_2[sim_2]
            N_points_2 = Number_points_2[sim_2]
            variable_2 = np.linspace(start_2, end_2, num=N_points_2)

        Dico_2 = Dictionnaries_2[sim_2]


        count = 0.0
        for var_2 in variable_2:

            for var_1 in variable_1:

                configuration[Dico_2][Param_2] = var_2
                configuration[Dico_1][Param_1] = var_1

                # update dictionnaries here #####
                # you have to access keys through configuration, not directly
                # trough their respective dictionnaries for example:
                #configuration['dictionnary to update']['key to update']



                ##################################


                f=open(configuration['filename'], 'a')

                if Parameters_2 == ['FluidType'] or Parameters_2 == ['corrPD'] or Parameters_2 == ['layout']:
                    f.write('\n' +Parameters_names_2[sim_2]+' = '+str(count)+'\n')

                else:
                    f.write('\n' +Parameters_names_2[sim_2]+' = '+str(var_2)+'\n')

                f.write(Parameters_names_1[sim_1]+' = '+str(var_1)+'\n\n')
                f.close()

                simu = Simulation()

                simu.startSimulation(configuration)

            count +=1

        sim_1 += 1

    sim_2 += 1
    sim_1 = 0


f=open('status.txt', 'a')
f.write('Simulation completed')
