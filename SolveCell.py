import math
import numpy as np

from properties import get_properties
from CoolProp.CoolProp import PropsSI

from pressureDrop import cell_pressureDrop
from feenstraCorrelation import cell_voidFraction
from vaporQuality import cell_vaporQuality
from energyBalance import EnergyBalance
from energyBalance import deriv_EnergyBalance
from q_dnb import q_dnb
from heatTransferCoefficient import*

from error import Error





def SolveCell(opCond, geom, Th_in, Tc_in, Ph_in, Pc_in, eps_in, xc_in ):

	'''
	#### Main Loop ###
	Main loop until the output pressure is converged :
		1) Compute output water temperature (Th_out) using energy balance function
		and newton method.
		2) Compute the vapor quality of the working fluid (xc_out)
		3) Compute the void fraction of the working fluid at the output (eps_out)
		4) Compute the pressure drop and the output pressure of the working fluid (pc_out)
		5) Update the value of the output working fluid temperature (Tc_out) using PropsSI
		6) Loop until Pc_out never change anymore
	'''
	# Numerical parameters
	kpmax = 10000
	tolP = 1e-6
	errorPc = 100
	errorPh = 100


	# Initialization of the variables
	kp = 0
	# Definition of Tc_out : equal to Tc_in since we take into account only evaporation
	# FIRST GUESS since the temperature will change with the decrease of pressure
	Tc_out = Tc_in*0.99
	prevPc_out = 0.0
	prevPh_out = 0.0

	print('\nFIRST ITERATE in the Pressure Loop')

	while (errorPc > tolP and errorPh > tolP and kp < kpmax):

		Q_rest = 0.0

		if 1:

			'''
			#### 1) Water Temperature calculation ####
			The output water temperature (Th_out) is calculated using the newton method.
			The stopping criterion is based on the error between Th_out and the previous
			iteration.
			'''

			# Newton method used to solve Th_out
			ktmax = 1000
			tol = 1e-6

			errest = 10
			h=0.01
			kt = 0

			# Initial guess on the temperature
			prevTh_out = Th_in*0.99

			try:

				while (errest > tol and kt < ktmax):

					#print(prevTh_out)
					#print(EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in, prevTh_out, Tc_out))
					#print(deriv_EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in, prevTh_out, Tc_out, h))

					Th_out = prevTh_out - EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in, prevTh_out, Tc_out)['balance']\
						/deriv_EnergyBalance(opCond, geom, Th_in, Tc_in, Pc_in, eps_in, prevTh_out, Tc_out, h)

					errest = abs(Th_out - prevTh_out)
					prevTh_out = Th_out
					kt = kt + 1

				if (kt == ktmax):
					print('WARNING : Hot temperature calculation did not converged with %d iterations. \n' %ktmax)
					print('You can increase the Number of iterations or change the initial value (Th_out) inside the function')
				else:
					print('Water temperature value at output (Th_out): %.3f. Calculation converged in %d iterations. \n' %(Th_out,kt))

			except Exception as e:
				raise Error('Newton',e)

		'''
		#### 2) Vapor Quality calculation ####
		'''

		[xc_out, hc_in, hc_out, Q_rest] = cell_vaporQuality(opCond, geom, Th_in, Th_out, Tc_in, xc_in )
		print('Working fluid vapor quality value (xc_out): %.5f. \n' %(xc_out))

		if Q_rest>0:
			Th_out = Th_out + 1e3*Q_rest/(opCond['mdot_h']*1/4*math.pi*(geom['D']-2*geom['t'])**2*PropsSI('C','T',Th_out,'Q',0.0,'Water'))

		'''
		#### 3) Void Fraction calculation ####
		'''

		eps_out = cell_voidFraction(opCond, geom, xc_out, Tc_out, eps_in )
		print('Working fluid void fraction value (eps_out): %.3f. \n' %(eps_out))

		'''
		#### 4) Pressure drop calculation inside the cell ####
		'''
		[Ph_out, Pc_out] = cell_pressureDrop(opCond, geom, Th_out, Tc_out, Pc_in, Ph_in, eps_in, eps_out, xc_out)
		print('Working fluid pressure value at output (Pc_out): %.3f. \n' %(Pc_out))

		'''
		#### 5) Compute working fluid temperature using the pressure drop calculated ####
		'''
		Tc_out = PropsSI('T','P',Pc_out,'Q',xc_out,opCond['FluidType'])
		print('Tc_out: %.5f \n' %Tc_out)


		#########
		kp = kp + 1

		errorPc = abs(Pc_out - prevPc_out)
		prevPc_out = Pc_out

		errorPh = abs(Ph_out - prevPh_out)
		prevPh_out = Ph_out

		print('End of Iterate number : %d \n' %kp)

	if (kp == kpmax):
		print('WARNING : Pressure drop calculation did not converged with %d iterations. \n' %kpmax)
		print('You can increase the Number of iterations or change the initial value (Th_out) inside the function')
	else:
		print('\nPressure value Pc_out: %.3f. Calculation converged in %d iterations. \n' %(Pc_out,kp))


	#### Check second energy balance
	A = geom['s']*geom['dx'] # cell bottom surface /!\ this will change with tubes geometries
	mdot_c = opCond['mdot_c']*A

	cp_hi = PropsSI('C','T',Th_out,'Q',0.0,'Water')/1000 #[kJ/kg.K]
	mdot_h = opCond['mdot_h']*1/4*math.pi*(geom['D']-2*geom['t'])**2 # [kg/s]
	Q = mdot_h*cp_hi*abs(Th_out-Th_in) # [kW]

	print('Bilan 2 : %.6f ' %(mdot_c*(hc_out- hc_in) - Q))

	q = Q/(math.pi*geom['D']*geom['dx'])
	if q > q_dnb(opCond, geom, Tc_out):
		print('WARNING : departure from nucleate boiling reached (q : %.3f, q_dnb : %.3f)' %(q,q_dnb(opCond, geom, Tc_out)))
	else:
		print('q : %.3f, q_dnb : %.3f' %(q,q_dnb(opCond, geom, Tc_out)))


	# Capacity of the cell
	Qcell = Q #[kW]
	OtherData={}
	OtherData['alpha_a'] = outerHeatTransfer(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out)
	OtherData['alpha_i'] = innerHeatTransfer(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out)[0]
	#OtherData['kt']=kt
	#OtherData['kp']=kp
	#OtherData['Bilan2']=(mdot_c*(hc_out- hc_in) - Q)

	return [Ph_out, Pc_out, Th_out, Tc_out, xc_out, eps_out, Qcell, OtherData]



# wait = input("PRESS ENTER TO CONTINUE.")
