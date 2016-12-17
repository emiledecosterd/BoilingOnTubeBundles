import math
from properties import get_properties
from CoolProp.CoolProp import PropsSI

def innerHeatTransfer(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out):

# Constants calculations :
	p_crit = PropsSI('pcrit',opCond['FluidType']) #[Pa]

	geom['dx'] = geom['L']/geom['n'] # [m]
	A = math.pi*geom['D']*geom['dx'] # [m^2] external surface of tube section

	mdot_h = opCond['mdot_h']*0.25*math.pi*(geom['D']-2.0*geom['t'])**2.0 # [kg/s]
	cp_hi = PropsSI('C','T',Th_in,'Q',0.0,'Water') # [J/kg/K]


	mu_h=PropsSI('V','T',Th_in,'Q',0.0,'water') # [Pa s]
	k_h=PropsSI('conductivity','T',Th_in,'Q',0.0,'water') # [W/m/K]

	Pr = cp_hi*mu_h/k_h # [-] Prandlt number

	Re_D = 4.0*mdot_h/(mu_h*math.pi*(geom['D']-2.0*geom['t'])) # [-] Reynolds number
<<<<<<< HEAD
	#print('Re_D')
	#print(Re_D)
=======
	print('Re_D')
	print(Re_D)
>>>>>>> PlotsPresentation
	f = (1.8*math.log10((6.9/Re_D)+(geom['e_i']/((geom['D']-2.0*geom['t'])*3.7))**1.11))**-2.0 # [-] friction factor for rough pipes
	Re_e = Re_D*(geom['e_i']/(geom['D']-2.0*geom['t']))*(f/8.0)**0.5 # [-] Roughness Reynolds number
	#print('Re_e')
	#print(Re_e)
	if Re_e < 35 :
		# Hydrodynamically Smooth model
		f = (0.79*math.log(Re_D)-1.64)**-2.0 # [-] friction factor for smooth pipes
		Nu = ((f/8.0)*(Re_D-1000.0)*Pr)/(1.0+12.7*(f/8.0)**0.5*(Pr**(2.0/3.0)-1.0)) # [-] Nusselt number
	else:
		# Hydrodynamically Rough-walled pipes
		Nu = ((f/8.0)*Re_D*Pr)/(1.0+(f/8.0)**0.5*(4.5*Re_e**0.2*Pr**0.5-8.48)) # [-] Nusselt number

	# Inner Heat transfer coefficient alpha_i :
	alpha_i = Nu*k_h/((geom['D']-2.0*geom['t'])) # [W/m^2/K]

	return(alpha_i,f)

def outerHeatTransfer(opCond, geom, Th_in, Tc_in, Pc_in, eps_in,Th_out, Tc_out):
	# Constants calculations :
	p_crit = PropsSI('pcrit',opCond['FluidType']) #[Pa]

	geom['dx'] = geom['L']/geom['n'] # [m]
	A = math.pi*geom['D']*geom['dx'] # [m^2] external surface of tube section
	mdot_h = opCond['mdot_h']*0.25*math.pi*(geom['D']-2.0*geom['t'])**2.0 # [kg/s]
	cp_hi = PropsSI('C','T',Th_in,'Q',0.0,'Water') # [J/kg/K]

	### Calculation of alpha_a (outer heat transfer coefficient)
	if geom['corr'] == 'Cooper': #according to Cooper correlation

		p_r = Pc_in/p_crit # [-]

		M = PropsSI('M',opCond['FluidType'])*1e3 # [g/mol]

		if p_r < 0.001 or p_r > 0.9 or M < 2 or M > 200 :
			raise Exception('This correlation will not give satisfying model for these values')

		else :

			q = mdot_h*cp_hi*(Th_in-Th_out)/A # [W/m^2]

			alpha_a = 55*p_r**(0.12-0.08686*math.log(geom['e_o']*1e6))*\
			(-0.4343*math.log(p_r))**-0.55*M**-0.5*abs(q)**0.67 # [W/m^2/K]



	elif geom['corr'] == "Gorenflo":

		# reference values
		p_ro = 0.1 # reduced pressure
		R_po = 0.4 # rugosity [\mu m]
		q_0 = 20000 # heat flux [W/m^2]

		# get gorenflo alpha_0
		try:
			prop = get_properties(Tc_out, opCond['FluidType'])
		except Exception as error:
			print(error)
			return 0

		alpha_0 = prop['alpha_0'] # [W/m^2/K]

		R_p = geom['e_o']*1e6 # [\mu m]

		if alpha_0 == None:
			raise Exception('Gorenflo reference heat tranfser coefficient alpha_0 is not known, see Enginnering Databook III tab 9.2')

		elif opCond['FluidType'] == "Water" or opCond['FluidType'] == "Helium":

			q = mdot_h*cp_hi*(Th_in-Th_out)/A # [W/m^2]
			p_r = Pc_in/p_crit # [-]
			F_pf = 1.73*p_r**0.27+(6.1+0.68/(1-p_r))*p_r**2
			nf = 0.9-0.3*p_r**0.15
			alpha_a = alpha_0*F_pf*(q/q_0)**nf*(R_p/R_po)**0.133 # [W/m^2/K]

		else:

			q = mdot_h*cp_hi*(Th_in-Th_out)/A
			p_r = Pc_in/p_crit
			F_pf = 1.2*p_r**0.27+2.5*p_r+p_r/(1-p_r)
			nf = 0.9-0.3*p_r**0.3
			alpha_a = alpha_0*F_pf*(q/q_0)**nf*(R_p/R_po)**0.133 # [W/m^2/K]


	else : #default is Mostinski
		p_r = Pc_in/p_crit
		Fp = 1.8*p_r**0.17+4*p_r**1.2+10*p_r**10

		q = mdot_h*cp_hi*(Th_in-Th_out)/A # [W/m^2]
		alpha_a = 0.00417*abs(q)**0.7*(p_crit/1000.0)**0.69*Fp # [W/m^2/K]

	return(alpha_a)
