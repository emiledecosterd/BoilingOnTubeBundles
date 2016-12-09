import math
import numpy as np

from properties import get_properties
from CoolProp.CoolProp import PropsSI
from heatTransferCoefficient import*
from error import Error

'''
#### Energy balance function used to solve Th_out with the newton method ####
'''
def EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out):

	''' This function returns f evaluated in Th_out and Tc_out is set as equal to Tc_in (only evaporation)
	f is an energy balance
	f = UALMTD-mdot_h cp_hi (Th_in-Th_out)
	'''

	# Constants calculations :
	p_crit = PropsSI('pcrit',opCond['FluidType']) #[Pa]

	geom['dx'] = geom['L']/geom['n'] # [m]
	A = math.pi*geom['D']*geom['dx'] # [m^2] external surface of tube section
	mdot_h = opCond['mdot_h']*1/4*math.pi*(geom['D']-2*geom['t'])**2 # [kg/s]
	cp_hi = PropsSI('C','T',Th_in,'Q',0.0,'Water') # [J/kg/K]

	try:
		# Inner heat transfer coefficient
		alpha_i,f = innerHeatTransfer(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out)

		# Outer heat tranfer coefficient
		alpha_a = outerHeatTransfer(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out)
	except Exception as e:
		raise Error('alpha_i or alpha_a computation', e+'PropsSI failed, temperature not compatible')

	if opCond['TubeMat'] == 'copper':
		lam = 410 # [W/m/K]
	elif opCond['TubeMat'] == 'aluminium':
		lam = 273 # [W/m/K]
	elif opCond['TubeMat'] == 'steel':
		lam = 30 # [W/m/K]
	else :
		lam = opCond['TubeThermalConductivity'] # [W/m/K]


	U = (geom['D']/((geom['D']-2*geom['t'])*alpha_i)\
	+geom['D']/(2*lam)*math.log(geom['D']/(geom['D']-2*geom['t']))\
	+1/alpha_a)**(-1) # [W/m^2/K] calculation of U

	try:
		LMTD = ((Th_out-Tc_out)-(Th_in-Tc_in))/\
		(math.log((Th_out-Tc_out)/(Th_in-Tc_in))) # [K] calculation of LMTD
	except Exception as e:
		raise Error('Error in LMTD (energyBalance)', 'cell size is likely to be too large. Advice: increase n')


	# Tests :
	# f = U*A*LMTD-mdot_h*cp_hi*(Th_in-Th_out)
	#print('U : %.3f ,A : %.3f, LMTD %.3f, f : %.3f' %(U,A ,LMTD, f))

	#print('alpha_i : %.3f, alpha_a : %.3f, U : %.3f' %(alpha_i, alpha_a, U))
	output={}
	output['alpha_a']=alpha_a
	#output['alpha_i']=alpha_i
	output['balance']=U*A*LMTD-mdot_h*cp_hi*(Th_in-Th_out)
	# add here other information to send to solvecell


	return output # [W]-[W]

def deriv_EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out, h):
	df = (EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out+h, Tc_out)['balance']\
	 - EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out-h , Tc_out)['balance'])/(2*h)
	return(df)
