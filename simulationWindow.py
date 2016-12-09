##	@package simulationWindow
#
#	Handles everything related to user input

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from simulationWindowGUI import  Ui_MainWindow

##	SimulationWindow
#
#	The main window of the programm 
#	Handles user input 
#	Displays basic info to help create the simulation inputs
class SimulationWindow(Ui_MainWindow):

	##	__init__() The constructor
	#	@param window The reference to a QMainWindow object
	def __init__(self, window):

		Ui_MainWindow.__init__(self)
		self.window = window
		self.setupUi(window)


##	QResizableMainWindow
#
#	This class catches the resize event from the 'QMainWindow' class
#	and sends a signal
class QResizableMainWindow(QtWidgets.QMainWindow):

	resized = QtCore.pyqtSignal()

	def resizeEvent(self, resizeEvent):
		self.resized.emit()


