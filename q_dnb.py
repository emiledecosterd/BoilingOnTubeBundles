import math
from CoolProp.CoolProp import PropsSI


def q_dnb(opCond, geom, Tc_out):

    prop = {}
    prop['mu_L'] = PropsSI('V', 'T', Tc_out, 'Q', 0.0, opCond['FluidType'])
    prop['mu_G'] = PropsSI('V', 'T', Tc_out, 'Q', 1.0, opCond['FluidType'])
    prop['rho_L'] = PropsSI('D', 'T', Tc_out, 'Q', 0.0, opCond['FluidType'])
    prop['rho_G'] = PropsSI('D', 'T', Tc_out, 'Q', 1.0, opCond['FluidType'])

    prop['h_LG'] = (PropsSI('H','T',Tc_out,'Q',1.0,opCond['FluidType'])-\
    	PropsSI('H','T',Tc_out,'Q',0.0,opCond['FluidType']))/1000

    prop['sigma'] = PropsSI('I','T',Tc_out,'Q',1.0,opCond['FluidType'])

    C = 0.9

    q_dnb = C*(math.pi/24)*prop['rho_G']**0.5*prop['h_LG']*\
    (9.81*(prop['rho_L']-prop['rho_G'])*prop['sigma'])**0.25 # [kW/m^2]

    return(q_dnb)
