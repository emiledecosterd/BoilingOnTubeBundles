import sys
import math

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainWindow import MainWindow
from drawing import PipeDrawing
import numpy as np
#from mainSimulation import Simulation

from simulation import Simulation
from error import Error

'''
/!\
	MAKE GUI CLASS QOBJECT SUBCLASS!!! 
	QtWidgets.QWidget
/!\
'''

class MainController(QObject):

	# Simulation inputs
	opCond = {}
	geom = {}
	flowInputs = {}

	# For the parametric simulation
	current_Tc = 0
	current_Th = 0
	current_Ph = 0
	step = 0
	current_step = 0
	total = 1

	# Signals emitted by the main controller
	simulate = pyqtSignal(dict)
	progressUpdated = pyqtSignal(float)

	def __init__(self, app):

		super(MainController, self).__init__(app)

		# Fire main window
		window = QMainWindow()
		self.mainWindow = MainWindow(window)
		window.show()

		# Setup filemanager

		# Setup simulation
		self.setupSimulation()

		# Setup plotter
		self.long_plotter = PipeDrawing(self.mainWindow.long_GraphicsView)
		self.long_plotter.drawOuterRect()

		# Setup window
		self.mainWindow.updateDrawings.connect(self.redrawGeometry)
		self.mainWindow.setup()
		self.mainWindow.startSimulation.connect(self.startSimulation)
		self.mainWindow.stopSimulation.connect(self.forceQuit)

		# Launch application
		sys.exit(app.exec_())


	## SIMULATION

	def setupSimulation(self):
		print('Setup simulation')

		self.simulation = Simulation()
		self.simulationThread = QThread()
		self.simulation.moveToThread(self.simulationThread)
		self.simulate.connect(self.simulation.run)
		self.simulation.simulationCompleted.connect(self.handleSimulationResults)
		self.simulation.progressUpdated.connect(self.on_updateProgress)
		self.simulation.errorOccured.connect(self.handleError)
		self.progressUpdated.connect(self.mainWindow.on_updateProgress)
		self.simulationThread.start()

		self.parent().aboutToQuit.connect(self.forceQuit)


	def handleError(self, err):
		print(err.message)

	def startSimulation(self, configuration):
		print('Sarting simulation')

		# Store the current configuration for the simulation
		self.flowInputs = configuration['flowInputs']
		self.opCond = configuration['opCond']
		self.geom = configuration['geom']

		# Initialize the simulation
		if not self.checkSimulation():
			# At this point, if checksimulation returns False, we do a non-parametric simulation
			self.flowInputs['Tc_in'] = self.flowInputs['Tc_start']
			self.flowInputs['Th_in'] = self.flowInputs['Th_start']
			self.flowInputs['Ph_in'] = self.flowInputs['Ph_start']
		else:
			self.total = self.flowInputs['steps']

		# Launch the simulation with updated parameters
		configuration = {'opCond': self.opCond, 'geom': self.geom, 'flowInputs':self.flowInputs}
		self.simulate.emit(configuration)
		print('Simulate emitted')


	def handleSimulationResults(self, results):
		print('Simulation finished')

		# Display results
		self.fillCells(results)

		# Check if we need to make another parametric simulation
		if self.checkSimulation():
			# Launch the simulation with updated parameters
			self.current_step = self.current_step + 1
			configuration = {'opCond': self.opCond, 'geom': self.geom, 'flowInputs':self.flowInputs}
			self.simulate.emit(configuration)
		else:
			# If not, hide progress bar and reset all parameters  
			self.mainWindow.simulation_progressBar.setProperty("visible", False)	
			self.step = 0
			self.current_Tc = 0
			self.current_Th = 0
			self.current_Ph = 0
			self.current_step = 1


	# Calculate parameters for the next simulation: returns true if it needs to continue
	def checkSimulation(self):

		if self.flowInputs['currentParam'] == 'Tc':
			if self.current_Tc == 0:
				start = self.flowInputs['Tc_start']
				end = self.flowInputs['Tc_end']
				self.step = math.fabs(start-end)/self.flowInputs['steps']
				self.current_Tc = self.flowInputs['Tc_start']
			if self.current_Tc + self.step > self.flowInputs['Tc_end']:
				return False
			else:
				self.current_Tc = self.current_Tc + self.step
				self.current_Th = self.flowInputs['Th_start']
				self.current_Ph = self.flowInputs['Ph_start']

		elif self.flowInputs['currentParam']  == 'Th':
			if self.current_Th == 0:
				start = self.flowInputs['Th_start']
				end = self.flowInputs['Th_end']
				self.step = math.fabs(start-end)/self.flowInputs['steps']
				self.current_Th = self.flowInputs['Th_start']
			if self.current_Th + self.step >= self.flowInputs['Th_end']:
				return False
			else:
				self.current_Th = self.current_Th + self.step
				self.current_Tc = self.flowInputs['Tc_start']
				self.current_Ph = self.flowInputs['Ph_start']
				

		elif self.flowInputs['currentParam']  == 'Ph':
			if self.current_Ph == 0:
				start = self.flowInputs['Ph_start']
				end = self.flowInputs['Ph_end']
				self.step = math.fabs(start-end)/self.flowInputs['steps']
				self.current_Ph = self.flowInputs['Ph_start']
			if self.current_Ph + self.step >= self.flowInputs['Ph_end']:
				return False
			else:
				self.current_Ph = self.current_Ph + self.step
				self.current_Th = self.flowInputs['Th_start']
				self.current_Tc = self.flowInputs['Tc_start']
				
		elif self.flowInputs['currentParam']  == 'None':
			print('No parametrization')
			return False

		self.flowInputs['Tc_in'] = self.current_Tc
		self.flowInputs['Th_in'] = self.current_Th
		self.flowInputs['Ph_in'] = self.current_Ph
		return True


	def on_updateProgress(self, progress):

		step = 100/self.total
		totalProgress = (self.current_step+progress)*step
		self.progressUpdated.emit(totalProgress)


	## FILE MANAGEMENT

	def saveConfiguration(self, filename, configuration):

		# Use the filemanager
		print('Saving configuration')

	def loadConfiguration(self):

		# Use the filemanager
		print('Loading configuration')


	## DRAWING MANAGEMENT

	def redrawGeometry(self, geom):
		self.geom = geom
		self.redrawLongitudinalPipes()

	def redrawLongitudinalPipes(self):
		geom = self.geom
		self.long_plotter.scene.clear()
		self.long_plotter.drawOuterRect()
		self.long_plotter.drawPipes(geom['Nt'])
		self.coordinates = self.long_plotter.drawCells(geom['Nt'], geom['n'])
		print('Drawing finished')


	def fillCells(self, results):

		self.long_plotter.fillCells(self.coordinates, results['Th'])


	### THREADING

	def forceQuit(self):
		if self.simulationThread.isRunning():
			self.simulationThread.terminate()
			self.simulationThread.wait()


if __name__ == '__main__':

	# Create application
	app = QApplication(sys.argv)

	# Initialize main controller
	controller = MainController(app)

	