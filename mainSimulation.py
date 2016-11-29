'''
Boilling on Tube Bundles : Main Code
'''

import math
import numpy as np

from properties import get_properties
from CoolProp.CoolProp import PropsSI

from feenstraCorrelation import ini_cell_voidFraction
from SolveCell import SolveCell
from mdothDesired import guessMassFlow
from Postprocess import *

from PyQt5.QtCore import QObject, pyqtSignal

class Simulation(QObject):

    # A signal emitted when progress has been updated
    progressUpdated = pyqtSignal(float) 
    # A signal emitted when the simulation is completed
    simulationComplete = pyqtSignal(dict)

    def startSimulation(self, configuration):

        '''
        #### Inputs settings ###
        The configuration dictionary contains following sub-dictionaries:
            -> opCond : All operatings conditions constants
                -> opCond['FluidType'] : Cold Fluid name according to the get_properties's Table
        		-> opCond['TubeMat'] : Tube material (copper aluminium steel)
                -> opCond['mdot_c'] : Mass flow of the coolant fluid [kg/m²s]    /!\ Unité /!\
                -> opCOnd['mdot_h'] : Mass flow of the hot fluid (water) [kg/m²s]
                -> opCond['TubeThermalConductivity'] : User defined thermal conductivity [W/mK]

            -> geom : All geometrical constants
                -> geom['Nt'] : Numbers of tubes [-]
                -> geom['Nt_col'] : Number of columns
                -> geom['L'] : Length of the tubes [m]
                -> geom['n'] : Number of discretized cells in tube direction [-]
                -> geom['s'] : Tube pitch [m]
                -> geom['D'] : Outer tube diameter [m]
                -> geom['e_o'] : outside tube surface roughness [m]
        		-> geom['e_i'] : inside tube surface roughness [m]
        		-> geom['dx'] : Tube cell size [m]
        		-> geom['t'] : Tube thickness [m]
        		-> geom['corr'] : which correlation to use, Mostinski, Cooper, Gorenflo (slow af)
                -> ADD HERE THE DEFINITION OF THE ONE YOU NEED

            -> flowInputs : Thermodynamics variable at the Cold and Hot Fluid entrance
                -> flowInputs['Tc_in'] : Inlet Cold temperature in the shell [K]
                -> flowInputs['Th_in'] : Inlet Hot temperature in the tubes [K]
                -> flowInputs['Pc_in'] : Pressure at the cold fluid entrance [Pa]
                -> flowInputs['Ph_in'] : Pressure at the hot fluid entrance [Pa]
                -> flowInputs['xc_in'] : Vapor quality at the Cold fluid entrance [-]

        Note that all the Cold Fluid properties will be imported using Emile's get_properties
        function, while all the Hot Fluid properties can be imported with CoolProp function.
        '''
        opCond = configuration['opCond']
        geom = configuration['geom']
        flowInputs = configuration['flowInputs']

        geom['N'] = geom['Nt']*geom['Nt_col']

        Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])


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




        '''
        #### Main Loop ###
        In this main loop, we apply the SolveCell function on the whole domain.
        '''
        Qtot = 0.0

        totalLoops = (geom['Nt'])*(geom['n'])
        currentLoop = 0

        # ForLoop over the domain to compute T, x, and eps
        for i in range(1, geom['Nt']+1):
            for j in range(1, geom['n']+1):

                # Let know where we are in the simulation
                currentLoop = currentLoop+1
                self.progressUpdated.emit(currentLoop/totalLoops)

                np.set_printoptions(precision=3)
                print(xc)
                print(OtherData)
                print(Th)

        print('Calculation complete !\n')



        Ph_drop = Ph[ geom['Nt'],geom['n']]-flowInputs['Ph_in']
        Pc_drop = Pc[ geom['Nt'],geom['n']]-Pc_in
        Th_drop = Th[ geom['Nt'],geom['n']]-flowInputs['Th_in']
        Tc_drop = Tc[ geom['Nt'],geom['n']]-flowInputs['Tc_in']
        xc_drop = xc[ geom['Nt'],geom['n']]-flowInputs['xc_in']

        # q = Qtot/(geom['Nt']*math.pi*geom['D']*geom['L'])  # [kW/m²]
        Q=Qtot*geom['Nt_col'] # [kW]


        print('Ph_drop')
        print(Ph_drop)
        print('Pc_drop')
        print(Pc_drop)
        print('Th_drop')
        print(Th_drop)
        print('Tc_drop')
        print(Tc_drop)
        print('xc_drop')
        print(xc_drop)
        print('Heat transfer Q [kW] %.3f :' %Q)

        ################################################################################
        #               Postprocessing

        plot_boiler(Th, Ph, Tc, Pc, xc, eps, geom['n'], geom['Nt'])
        plot_xc_pipe(xc, geom['n'], geom['Nt'])

        input()

        self.results = {
            'Th' : Th,
            'Ph' : Ph, 
            'Tc' : Tc,
            'Pc' : Pc, 
            'xc' : xc,
            'Q': Q
        }
        self.simulationComplete.emit(self.results)
        return
