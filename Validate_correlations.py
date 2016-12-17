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


################################################################################
#                       Pressure Drop (Single Phase)

files = glob.glob('./Validation/Pressure_Drop/*.txt')
for f in files:
    os.remove(f)

geom['D'] = 18.87e-3
geom['s'] = 22.22e-3
geom['sh'] = 22.22e-3
geom['layout'] = 'Staggered'
opCond['FluidType'] = 'R134a'

start = 4
end = 40
mdot_c_range = np.linspace(start, end, num= 15)

Tc = 273.15 + 14 #14°C

mu = PropsSI('V', 'T', Tc, 'Q', 0.0, opCond['FluidType'])
rho = PropsSI('D', 'T', Tc, 'Q', 0.0, opCond['FluidType'])


corrPDs = ['Gaddis', 'Zukauskas']


for corrPD in corrPDs:
    if corrPD == 'Zukauskas':
        
        for mdot_c in mdot_c_range:
            f=open('./Validation/Pressure_Drop/Pressure_Drop_res.txt','a')
            f.write('corrPD = '+str(2)+'\nG_{wf,sp} = '+str(mdot_c)+'\n\n')

            Re = mdot_c*geom['D']/mu

            if Re < 1000:
                Eu = 0.795 + 0.247e3/Re + 0.335e3/math.pow(Re,2) - 0.155e4/math.pow(Re,3) + 0.241e4/math.pow(Re,4)
            else:
                Eu = 0.245 + 0.339e4/Re - 0.984e7/math.pow(Re,2) + 0.132e11/math.pow(Re,3) - 0.559e13/math.pow(Re,4)

            f1 = Eu/4  # Single-Phase friction factor

            deltaPf = 4*f1*mdot_c**2*geom['Nt']/(2*rho)

            f=open('./Validation/Pressure_Drop/Pressure_Drop_res.txt','a')
            f.write('\Delta\,P_{frictional}[Pa] = '+str(deltaPf)+'\n\n')

    elif corrPD == 'Gaddis':
        for mdot_c in mdot_c_range:
            f=open('./Validation/Pressure_Drop/Pressure_Drop_res.txt','a')
            f.write('corrPD = '+str(1)+'\nG_{wf,sp} = '+str(mdot_c)+'\n\n')

            Re = mdot_c*geom['D']/mu

            ## Gaddis and Gnielinski for single pressure drop

            # Geometry parameters
            a = geom['sh']/geom['D']
            b = geom['s']/geom['D']
            c = math.sqrt((a/2)**2+b**2)

            # Compute the viscosity correction factor for laminar and turbulent flow
            # mu_eq_wall = propWall['mu_L']*(1-eps_out)+propWall['mu_G']*eps_out
            # fzl = (mu_eq_wall/mu_eq)**(0.57/(((4*a*b/math.pi)-1)*Re)**0.25)
            # fzt = (mu_eq_wall/mu_eq)**(0.14)

            fzl = 1
            fzt = 1

            if geom['layout'] == 'InLine':
                # Laminar flow in line pressure drop coefficient
                flf = (280*math.pi*(b**0.5-0.6)**2+0.75)/((4*a*b-math.pi)*a**1.6)
                zeta_lf = flf/Re

                # Turbulent flow in line pressure drop coefficient
                ftf = (0.22+1.2*((1-0.94/b)**0.6)/((a-0.85)**1.3))*10**(0.47*(b/a-1.5))+ \
                    (0.03*(a-1)*(b-1))
                zeta_tf = ftf/(Re**(0.1*b/a))

                # Inlet/Outlet pressure losses influence
                if (geom['Nt'] >= 5) and (geom['Nt'] <= 10):
                    fnt = (1/a**2)*(1/geom['Nt']-1/10)
                else:
                    fnt = 0.;

                # Pressure drop coefficient
                zeta = zeta_lf*fzl + (zeta_tf*fzt + fnt)*(1-math.exp(-(Re+1000)/2000))

            if geom['layout'] == 'Staggered':
                # Staggered perpendicular
                if (b >= 0.5*math.sqrt(a+1)):
                    # Laminar flow staggered type pressure drop coefficient
                    flv = (280*math.pi*(b**0.5-0.6)**2+0.75)/((4*a*b-math.pi)*a**1.6)

                    # Inlet/Outlet pressure losses influence
                    if (geom['Nt'] >= 5) and (geom['Nt'] <= 10):
                        fnt = (1/a**2)*(1/geom['Nt']-1/10)
                    else:
                        fnt = 0.;

                # Stagerred diagonal
                elif (b < 0.5*math.sqrt(a+1)):
                    # Laminar flow staggered type pressure drop coefficient
                    flv = (280*math.pi*(b**0.5-0.6)**2+0.75)/((4*a*b-math.pi)*c**1.6)

                    # Inlet/Outlet pressure losses influence
                    if (geom['Nt'] >= 5) and (geom['Nt'] <= 10):
                        fnt = (2*(c-1)/(a*(a-1)))**2*(1/geom['Nt']-1/10)
                    else:
                        fnt = 0.;

                # Laminar flow staggered type pressure drop coefficient
                zeta_lv = flv/Re

                # Turbulent flow staggered type pressure drop coefficient
                ftv = 2.5+1.2/((a-0.85)**1.08)+0.4*(b/a-1)**3-0.01*(a/b-1)**3
                zeta_tv = ftv/(Re**0.25)

                # Pressure drop coefficient
                zeta = zeta_lv*fzl + (zeta_tv*fzt + fnt)*(1-math.exp(-(Re+200)/1000))

            # Single-Phase friction coefficient
            f1 = zeta

            deltaPf = 4*f1*mdot_c**2*geom['Nt']/(2*rho)

            f=open('./Validation/Pressure_Drop/Pressure_Drop_res.txt','a')
            f.write('\Delta\,P_{frictional}[Pa] = '+str(deltaPf)+'\n\n')
