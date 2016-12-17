##	@package simulationThread
#	Contains a subclass of QThread

import sys
from PyQt5 import QtGui, QtCore, QtWidgets

##	SimulationThread
#	Implements two method to communicate with the main simulation loop with signals
class SimulationThread(QtCore.QThread):

	stopSimulationRequested = False

	def stopSimulation(self):
		self.stopSimulationRequested = True

	def reset(self):
		self.stopSimulationRequested = False
		
