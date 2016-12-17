import math
import numpy as np
from CoolProp.CoolProp import PropsSI

'''
#### Vapor Quality calculation ####
Based on the following equation : h = x*H_LG + H_L

H_LG : Latent heat of vaporization
H_L : Sensible heat
'''

def cell_vaporQuality(opCond, geom, Th_in, Th_out, Tc_in, xc_in ):
    # Inlet enthalpy of the working fluid (cold)
    hc_in = PropsSI('H','T',Tc_in,'Q',xc_in,opCond['FluidType'])/1000 #[kJ/kg]

    # Others properties of working fluid flux
    prop = {}
    prop['h_L'] = PropsSI('H','T',Tc_out,'Q',0.0,opCond['FluidType'])/1000 #[kJ/kg]
    prop['h_LG'] = (PropsSI('H','T',Tc_out,'Q',1.0,opCond['FluidType'])-\
        PropsSI('H','T',Tc_out,'Q',0.0,opCond['FluidType']))/1000 #[kJ/kg]

    A = geom['s']*geom['dx'] # cell bottom surface /!\ this will change with tubes geometries
    mdot_c = opCond['mdot_c']*A # [kg/s]

    # Properties of water flux
    cp_hi = PropsSI('C','T',Th_out,'Q',0.0,'Water')/1000 #[kJ/kg.K]
    mdot_h = opCond['mdot_h']*1/4*math.pi*(geom['D']-2*geom['t'])**2 # [kg/s]
    Q = mdot_h*cp_hi*abs(Th_out-Th_in) # [kW]

    # Outlet enthalpy of the working fluid
    hc_out = Q/mdot_c + hc_in # [kJ/kg]

    # Calculation of vapor quality
    xc_out = (hc_out-prop['h_L'])/prop['h_LG'] # get_propeties and PropsSI give the same h_LG
    Q_rest = 0

    if xc_out > 1:
        xc_out = 1
        Q_rest = mdot_c*(hc_out-(prop['h_L']+prop['h_LG'])) # kg/s * kJ/kg = kJ/s = kW 
        hc_out = prop['h_L']+prop['h_LG']

    #print('Q : %.3f, hc_in: %.3f, hc_out : %.3f, Hl: %.3f, HG: %.3f, Cp : %.3f, mdot_h : %.3f' %(Q, hc_in, hc_out,prop['h_L'],prop['h_LG'],cp_hi,mdot_h ))


    return(xc_out, hc_in, hc_out, Q_rest)
