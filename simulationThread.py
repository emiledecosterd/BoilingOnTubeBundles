import sys

# PyQt classes
from PyQt5 import QtGui, QtCore, QtWidgets

class SimulationThread(QtCore.QThread):

	stopSimulationRequested = False

	def stopSimulation(self):
		self.stopSimulationRequested = True

	def reset(self):
		self.stopSimulationRequested = False
		
