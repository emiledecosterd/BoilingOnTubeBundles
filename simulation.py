##	@package simulation
#	Link between the solver script and the GUI	

# Packages for the simulation
import math
import numpy as np
from CoolProp.CoolProp import PropsSI
from feenstraCorrelation import ini_cell_voidFraction
from SolveCell import SolveCell


# Qt and GUI packages
from PyQt5.QtCore import QObject, pyqtSignal, QThread
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
	resetSimulationStatusRequested = pyqtSignal()

	# In order to use this class from a script
	parallel = False

	##	Constructor
	#	@param 	parallel 	True if class should be used in GUI, False if used from script
	def __init__(self, parallelComputing):
		super(Simulation, self).__init__()
		self.parallel = parallelComputing

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

				if self.parallel:
					# Check if simulation should stop
					currentThread = QThread.currentThread()
					if currentThread.stopSimulationRequested:
						currentThread.reset()
						self.simulationCompleted.emit({})
						return

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

		print('INFO: Calculation complete !\n')

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
		return self.results 


##	defaultConfiguration()
#	@return	configuration Default parameters for the simulation so it does not have to be loaded each time
def defaultConfiguration():

	opCond = {
			'FluidType' : 'R134a',
			'mfr_c' : 40,
			'mfr_h' : 15,
			'TubeMat' : 'other',
			'TubeThermalConductivity' : 410
	}
	geom = {
		'Ds' : 1,
		'D' : 30e-3,
		'Nt' : 3,
		'Nt_col' : 4,
		'L' : 3.0,
		's' : 45e-3,
		'sh' : 45e-3,
		't' : 3e-3,
		'layout' : 'Staggered',
		'e_i' : 3e-6,
		'e_o' : 3e-6,
		'n' : 10,
		'corr' : 'Cooper',
		'corrPD' : 'Gaddis',
		'chosenResult' : 'xc'
	}
	flowInputs = {
		'Tc' : [268.15],
		'Th' : [298.15],
		'Ph' : [1e5],
		'xc_in' : 0.05,
		'param' : None
	}
	configuration = {
		'opCond' : opCond,
		'geom' : geom,
		'flowInputs' : flowInputs 
	}
	return configuration


