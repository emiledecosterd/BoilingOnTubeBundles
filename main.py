import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainWindow import MainWindow
from drawing import PipeDrawing
import numpy as np
#from simulationMain import Simulation

'''
/!\
	MAKE GUI CLASS QOBJECT SUBCLASS!!! 
	QtCore.QObject
/!\
'''

class MainController(QObject):

	# Signals emitted by the maincontroller
	simulate = pyqtSignal(dict)

	def __init__(self, app):

		super(MainController, self).__init__()

		# Fire main window
		window = QMainWindow()
		self.mainWindow = MainWindow(window, self)
		window.show()

		# Setup filemanager

		# Setup simulation
		self.simulationStopped = False
		self.setupSimulation()

		# Setup plotter
		self.plotter = PipeDrawing(self.mainWindow.geometry_GraphicsView)
		self.plotter.drawOuterRect()

		# Setup window
		self.mainWindow.setup()
		self.mainWindow.startSimulation.connect(self.startSimulation)
		self.mainWindow.stopSimulation.connect(self.stopSimulation)
	
		# Launch application
		sys.exit(app.exec_())


	## SIMULATION

	def setupSimulation(self):
		# Setup simulation
		print('Setup simulation')
		self.simulationThread = QThread()
		self.simulation = Simulation()
		self.simulation.moveToThread(self.simulationThread)
		self.simulate.connect(
			self.simulation.startSimulation)
		self.simulation.simulationComplete.connect(
			self.handleSimulationResults)
		self.simulation.simulationComplete.connect(
			self.mainWindow.on_run)
		self.simulation.progressUpdated.connect(
			self.mainWindow.on_updateProgress)
		self.simulationThread.start()

	def startSimulation(self, configuration):

		print('Sarting simulation')
		if self.simulationStopped:
			self.setupSimulation()
		
		self.simulate.emit(configuration)


	def stopSimulation(self):

		print('Stopping simulation')
		
		
		self.simulationThread.terminate()
		self.simulationThread.wait()
		#self.simulationThread = None
		self.simulationStopped = True


	def handleSimulationResults(self, results):

		print('Simulation finished')

		if results == {}:
			print('No results!')
		elif results is not None:
			self.fillCells(results)
		else:
			print('No results!!!')



	## FILE MANAGEMENT

	def saveConfiguration(self, filename, configuration):

		# Use the filemanager
		print('Saving configuration')

	def loadConfiguration(self):

		# Use the filemanager
		print('Loading configuration')


	## DRAWING MANAGEMENT

	def redrawSchema(self, setup):

		self.plotter.scene.clear()
		self.plotter.drawOuterRect()
		self.plotter.drawPipes(setup['Nt'])
		self.coordinates = self.plotter.drawCells(setup['Nt'], setup['n'])


	def fillCells(self, results):

		print('Painting results')
		self.plotter.fillCells(self.coordinates, results['Th'])



if __name__ == '__main__':

	# Create application
	app = QApplication(sys.argv)

	# Initialize main controller
	controller = MainController(app)

	