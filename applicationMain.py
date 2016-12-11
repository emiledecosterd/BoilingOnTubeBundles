##	@package applicationMain
#
#	The link between GUI, Simulation and PostProcessing

import sys
from copy import copy

# PyQt classes
from PyQt5 import QtGui, QtCore, QtWidgets

# Our classes
from pipePlotter import LongPipePlotter, TransvPipePlotter
from simulationWindow import SimulationWindow, QResizableMainWindow
from simulation import Simulation
from error import Error

##	MainController
#
#	Manages all the programm.
#	Launches the simulation, handles results and errors
class MainController(QtCore.QObject):

	# Instance variables
	isLongPlotter = True
	currentSimulationConfiguration = None
	results = None
	running = False
	simulationThread = None

	# Signals
	runSimulationRequested = QtCore.pyqtSignal(dict)


	##	The constructor
	#	@param app The application created in '__main__'
	def __init__(self, app):
		# Initialize superclass
		super(MainController, self).__init__(app)

		# Create simulation window
		window = QResizableMainWindow()
		self.mainWindow = SimulationWindow(window)
		self.mainWindow.setup()

		# Create the plotters
		self.longPlotter = LongPipePlotter(self.mainWindow.graphicsView)
		self.transvPlotter = TransvPipePlotter(self.mainWindow.graphicsView)

		# Setup the redirectioning of stdout to console
		self.console = Console()
		sys.stdout = self.console

		# Create the simulation and its thread
		simulation = Simulation()
		self.simulationThread = QtCore.QThread()
		simulation.moveToThread(self.simulationThread)
		self.simulationThread.finished.connect(simulation.deleteLater)
		simulation.progressUpdated.connect(self.updateProgress)
		simulation.simulationCompleted.connect(self.handleResults)
		simulation.errorOccured.connect(self.handleError)
		self.runSimulationRequested.connect(simulation.run)
		self.simulationThread.start()

		# Create the connexions
		self.console.printOccured.connect(self.mainWindow.printToConsole)
		self.mainWindow.changesOccured.connect(self.resetResults)
		self.mainWindow.changesOccured.connect(self.updatePlots)
		self.mainWindow.chosenResultChanged.connect(self.updatePlots)
		self.mainWindow.graphicsView.clicked.connect(self.togglePlotter)
		self.mainWindow.showPlotsButton.clicked.connect(self.showPlots)
		self.mainWindow.runButton.clicked.connect(self.startSimulation)
		window.resized.connect(self.updatePlots)

		# Show the window
		window.show()

		# Launch application
		# For more details: 
		# http://stackoverflow.com/questions/25075954/using-sys-exit-with-app-exec-in-pyqt
		sys.exit(app.exec_())

	##	The destructor
	def __del__(self):
		print('INFO: Quitting... Wait for thread to finish')
		self.simulationThread.quit()
		self.simulationThread.wait()


	##	startSimulation()
	#	Lauches the simulation after some verifications
	#	@param 	None
	def startSimulation(self):
		if self.running:
			print('INFO: Stopping simulation')
			self.running = False
			self.mainWindow.progressBar.setProperty('visible', False)
			self.mainWindow.runButton.setText('Run')
		else:
			# Load the current inputs in the GUI
			self.currentSimulationConfiguration = self.mainWindow.readConfiguration()
			flowInputs = copy(self.currentSimulationConfiguration['flowInputs'])
			try:
				# Store the number of simulations to do
				if flowInputs['param'] is not None:
					n = len(flowInputs[flowInputs['param']])
					self.currentSimulationConfiguration['flowInputs']['Nparam'] = n
				else:
					self.currentSimulationConfiguration['flowInputs']['Nparam'] = 1
			except Exception as e:
				error = Error('mainController.startSimulation', e)
				print(error)
				self.running = False
				self.mainWindow.progressBar.setProperty('visible', False)
				self.mainWindow.runButton.setText('Run')
				return

			# Change arrays to floats for the simulation. 
			# Take the last element of array so we can pop it at the end of the simulation.
			flowInputs['Tc_in'] = flowInputs['Tc'][-1]
			flowInputs['Th_in'] = flowInputs['Th'][-1]
			flowInputs['Ph_in'] = flowInputs['Ph'][-1]

			# Replace them in the configuration that will be sent to the solver.
			# Copy so that self.currentSimulationConfiguration does not change
			simulationConfiguration = copy(self.currentSimulationConfiguration)
			simulationConfiguration['flowInputs'] = flowInputs

			# Let the simulation begin!
			self.running = True
			#print(self.currentSimulationConfiguration)
			#print(simulationConfiguration)
			print('INFO: Starting simulation')
			self.mainWindow.progressBar.setProperty('visible', True)
			self.mainWindow.runButton.setText('Stop')
			self.runSimulationRequested.emit(simulationConfiguration)
		

	##	checkParam()
	#	Checks if a new simulation has to be launched based on the parametrization
	#	@return 	A boolean determining if yes or no a new simulation has to be started
	def checkParam(self):

		if self.currentSimulationConfiguration['param'] is None:
			return False
		else:
			flowInputs = self.currentSimulationConfiguration['flowInputs']
			n = len(flowInputs[flowInputs['param']])
			if n >= 1:
				return True
			else:
				return False


	##	updateProgress()
	#	Updates the progress bar in the GUI
	#	@param 	progress 	The progress in range [0-1]
	def updateProgress(self, progress):
		try:
			N = self.currentSimulationConfiguration['flowInputs']['Nparam']
		except Exception as e:
			error = Error('mainController.updateProgress', e)
			print('ERROR: %s' % e)

		fraction = 100/N
		if self.currentSimulationConfiguration['flowInputs']['param'] is not None:
			n = len(self.currentSimulationConfiguration['flowInputs']
				[self.currentSimulationConfiguration['param']])
		else:
			n = 1
		progress = (N-n)*fraction + progress
		self.mainWindow.progressBar.setProperty('value', progress)


	def handleResults(self, results):
		# Post process, no GUI
		self.results = results

		# Plot the result
		self.isLongPlotter = True
		self.mainWindow.setupInputs(self.currentSimulationConfiguration)
		self.updatePlots()

		# Update the parameters (remove the parameter for the just finished
		# simulation) and check if a new simulation should be launched
		param = self.currentSimulationConfiguration['flowInputs']['param']
		if param is not None:
			self.currentSimulationConfiguration['flowInputs'][self.currentSimulationConfiguration[param]].pop()
		if self.checkParam:
			self.runSimulationRequested.emit(self.currentSimulationConfiguration)
		else:
			print('INFO: Simulation finished!')
			self.showPlots()


	def handleError(self, error):
		print(error)
		print('INFO: Stopping simulation')
		self.running = False
		self.mainWindow.progressBar.setProperty('visible', False)
		self.mainWindow.runButton.setText('Run')


	##	updatePlots()
	#	Reads the user inputs from the main window and plots the geometry
	#	@param	None
	def updatePlots(self):

		try:
			configuration = self.mainWindow.readConfiguration()
			if self.isLongPlotter:
				self.longPlotter.drawScheme(configuration['geom'], self.results)
			else:
				self.transvPlotter.drawScheme(configuration['geom'])

		except Exception as e:
			print('ERROR: Error plotting the tube bundles. \nCheck your parameters (perhaps you put something to 0)')


	##	showPlots()
	#	Shows the resultsDialog to browse through all the plots
	#	@param 	None
	def showPlots(self):

		print('INFO: No plots available. Run a simulation to have some')


	##	togglePlotter()
	#	Change the plot we want to display
	#	@param	None
	def togglePlotter(self):
		if self.isLongPlotter:
			self.isLongPlotter = False
		else:
			self.isLongPlotter = True
		self.updatePlots()	


	def resetResults(self):
		self.results = None



##	Console
#
#	This class is meant to replace stdout to capture the 'print's
class Console(QtCore.QObject):

    printOccured = QtCore.pyqtSignal(str)

    ##	Takes the output and sends it via an emitted signal
    def write(self, text):
        self.printOccured.emit(str(text))

    ##	To replace stdout, must implement this
    #	http://stackoverflow.com/questions/20525587/python-logging-in-multiprocessing-attributeerror-logger-object-has-no-attrib
    def flush(self):
    	pass


if __name__ == '__main__':

	# Create the application
	app = QtWidgets.QApplication(sys.argv)

	# Create main controller that does everything
	controller = MainController(app)