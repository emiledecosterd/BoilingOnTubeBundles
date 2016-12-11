##	@package simulation
#	Link between the solver script and the GUI	

# Packages for the simulation
import math
import numpy as np
from properties import get_properties
from CoolProp.CoolProp import PropsSI
from feenstraCorrelation import ini_cell_voidFraction
from SolveCell import SolveCell

# Qt and GUI packages
from PyQt5.QtCore import QObject, pyqtSignal
from error import Error

##	Simulation
#
#	This class launches the simulation.
#	It will be run on a parallel thread and communicate through signals.
class Simulation(QObject):

	# Signals
	progressUpdated = pyqtSignal(float)
	simulationCompleted = pyqtSignal(dict)
	errorOccured = pyqtSignal(Error)

	##	run()
	#	This method launches the simulation
	#	@param	configuration	A dictionnary containing all the necessary informations for the simulation
	def run(self, configuration):

		# Set the inputs correctly
		opCond = configuration['opCond']
		geom = configuration['geom']
		flowInputs = configuration['flowInputs']

		# Compute missing parameters
		geom['N'] = geom['Nt']*geom['Nt_col']

		try:
			Pc_in = PropsSI('P','T', flowInputs['Tc_in'], 'Q', flowInputs['xc_in'], opCond['FluidType'])
		except Exception as e:
			self.errorOccured.emit(Error('Simulation.run', e))
			return

		# Initialisation
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

		# Main loop
		Qtot = 0.0


		total = geom['Nt']*geom['n']
		currentLoop = 0

		# ForLoop over the domain to compute T, x, and eps
		for i in range(1, geom['Nt']+1):
			for j in range(1, geom['n']+1):

				# Send current progress to controller
				currentLoop = currentLoop+1
				progress = currentLoop/total
				self.progressUpdated.emit(progress)

				# Propagate error if there is one
				try:
					[Ph[i,j], Pc[i,j], Th[i,j], Tc[i,j], xc[i,j], eps[i,j], Q, OtherData[i,j]] = SolveCell(opCond, geom, Th[i,j-1], Tc[i-1,j], Ph[i,j-1], Pc[i-1,j], eps[i-1,j], xc[i-1,j] )
					Qtot += Q
				except Error as e:
					self.errorOccured.emit(e)
					return

					np.set_printoptions(precision=3)
				#print(xc)
				#print(eps)
				#print(OtherData)
				#print(Th)

				print('Calculation complete !\n')

				Ph_drop = Ph[ geom['Nt'],geom['n']]-flowInputs['Ph_in']
				Pc_drop = Pc[ geom['Nt'],geom['n']]-Pc_in
				Th_drop = Th[ geom['Nt'],geom['n']]-flowInputs['Th_in']
				Tc_drop = Tc[ geom['Nt'],geom['n']]-flowInputs['Tc_in']
				xc_drop = xc[ geom['Nt'],geom['n']]-flowInputs['xc_in']

		# q = Qtot/(geom['Nt']*math.pi*geom['D']*geom['L'])  # [kW/m²]
		Q=Qtot*geom['Nt_col'] # [kW]

		self.results = {
			'Th' : Th,
			'Ph' : Ph,
			'Tc' : Tc,
			'Pc' : Pc,
			'xc' : xc,
			'Q': Q,
			'eps' : eps,
			'OtherData' : OtherData
		}
		self.simulationCompleted.emit(self.results)
		return


##	defaultConfiguration()
#	@return	configuration Default parameters for the simulation so it does not have to be loaded each time
def defaultConfiguration():

	opCond = {
		'FluidType' : 'R134a',
		'mfr_c' : 5.3,
		'mfr_h' : 15,
		'TubeMat' : 'steel',
		'TubeThermalConductivity' : 400
	}
	geom = {
		'Ds' : 0.5,
		'D' : 15e-3,
		'Nt' : 3,
		'Nt_col' : 2,
		'L' : 3.0,
		's' : 70e-3,
		'sh' : 70e-3,
		't' : 5e-3,
		'layout' : 'Staggered',
		'e_i' : 3e-6,
		'e_o' : 3e-6,
		'n' : 8,
		'corr' : 'Mostinski',
		'corrPD' : 'Gaddis',
		'chosenResult' : 'xc'
	}
	flowInputs = {
		'Tc' : [273.15],
		'Th' : [293.15],
		'Ph' : [1e5],
		'xc_in' : 0.13,
		'param' : None
	}
	configuration = {
		'opCond' : opCond,
		'geom' : geom,
		'flowInputs' : flowInputs 
	}
	return configuration


