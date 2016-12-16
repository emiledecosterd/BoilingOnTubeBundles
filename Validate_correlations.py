import math
import numpy as np


from CoolProp.CoolProp import PropsSI
from heatTransferCoefficient import*
from feenstraCorrelation import cell_voidFraction

import os
import glob



# delets all .txt files in folder
files = glob.glob('./Validation/*.txt')
for f in files:
    os.remove(f)


################################################################################
###                     EDIT BASE CONFIGURATION HERE                         ###

opCond = {}
geom = {}
flowInputs = {}

# Operating Conditions
opCond['FluidType'] = 'R134a'
opCond['mfr_c'] = 25
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
geom['e_o'] = 2.3e-6
geom['t'] = 5e-3
geom['corr'] = 'Cooper'
geom['corrPD'] = 'Gaddis'
geom['layout'] = 'InLine'
geom['N'] = geom['Nt']*geom['Nt_col']

# Flow Inputs
flowInputs['Tc_in'] = 10 + 273.15
flowInputs['Th_in'] = 15+ 273.15
flowInputs['Ph_in'] = 1e5
flowInputs['xc_in'] = 0.8
Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])

opCond['mfr_h'] = 20.0 #mfr_hGuess
opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

configuration={}
configuration['opCond'] = opCond
configuration['geom'] = geom
configuration['flowInputs'] = flowInputs


################################################################################


start = 5000
end = 14000
q_range = np.linspace(start, end, num=5)

Th_in = flowInputs['Th_in']
Th_out = 0.0

opCond['mdot_h'] = 4
opCond['mdot_c'] = 4
flowInputs['Tc_in'] = 10 + 273.15


geom['dx'] = geom['L']/geom['n'] # [m]
A = math.pi*geom['D']*geom['dx'] # [m^2] external surface of tube section
mdot_h = opCond['mdot_h']*0.25*math.pi*(geom['D']-2.0*geom['t'])**2.0 # [kg/s]
cp_hi = PropsSI('C','T',Th_in,'Q',0.0,'Water') # [J/kg/K]

correlation = ["Cooper","Mostinski","Gorenflo"]


for corr in correlation:

    for q in q_range:

        Th_out = Th_in-q*A/(mdot_h*cp_hi)

        geom['corr'] = corr
        a_a = outerHeatTransfer(opCond, geom, Th_in, flowInputs['Tc_in'], Pc_in, 0,Th_out, flowInputs['Tc_in'])
        f=open('./Validation/'+corr+'_a_nb.txt','a')
        f.write('q = '+str(q)+'\na_a = '+str(a_a)+'\n\n')
        f.close()



################################################################################
#                       Feenstra

geom["s"] = 0.1
geom["D"] = 0.05

opCond["mdot_c"] = 0.0
Tc_out = 15 +273.15

start = -2
end = 0
x_range = np.logspace(start, end, num=30)

eps_in = 0.1
xc_out = 0.0

start = 10
end = 80
mdot_c_range = np.linspace(start, end, num= 5)

for mdot_c in mdot_c_range:

    opCond["mdot_c"] = mdot_c

    for x in x_range:

        xc_out = x

        eps = cell_voidFraction(opCond, geom, xc_out, Tc_out, eps_in )

        eps_in = eps

        f=open('./Validation/Feenstra_eps.txt','a')
        f.write('x = '+str(x)+'\neps = '+str(eps)+'\n\n')
        f.close()
