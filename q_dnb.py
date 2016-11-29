import math
from properties import get_properties


def q_dnb(opCond, geom, Tc_out):

	prop = get_properties(Tc_out, opCond['FluidType'])

	C = 0.9

	q_dnb = C*(math.pi/24)*prop['rho_G']**0.5*prop['h_LG']*\
	(9.81*(prop['rho_L']-prop['rho_G'])*prop['sigma'])**0.25 # [kW/m^2]

	return(q_dnb)
