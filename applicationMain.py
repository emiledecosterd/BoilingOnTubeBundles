##	@package applicationMain
#
#	The link between GUI, Simulation and PostProcessing

import sys

# PyQt classes
from PyQt5 import QtGui, QtCore, QtWidgets

# Our classes
from simulationWindow import SimulationWindow, QResizableMainWindow
from error import Error

class MainController(QtCore.QObject):

	##	The constructor
	#	@param app The application created in '__main__'
	def __init__(self, app):
		# Initialize superclass
		super(MainController, self).__init__(app)

		# Create simulation window
		window = QResizableMainWindow()
		self.mainWindow = SimulationWindow(window)

		# Show the window
		window.show()

		# Launch application
		# For more details: 
		# http://stackoverflow.com/questions/25075954/using-sys-exit-with-app-exec-in-pyqt
		sys.exit(app.exec_())


if __name__ == '__main__':

	# Create the application
	app = QtWidgets.QApplication(sys.argv)

	# Create main controller that does everything
	controller = MainController(app)