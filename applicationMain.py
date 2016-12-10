##	@package applicationMain
#
#	The link between GUI, Simulation and PostProcessing

import sys

# PyQt classes
from PyQt5 import QtGui, QtCore, QtWidgets

# Our classes
from simulationWindow import SimulationWindow, QResizableMainWindow
from simulation import Simulation
from error import Error

##	MainController
#
#	Manages all the programm.
#	Launches the simulation, handles results and errors
class MainController(QtCore.QObject):

	##	The constructor
	#	@param app The application created in '__main__'
	def __init__(self, app):
		# Initialize superclass
		super(MainController, self).__init__(app)

		# Create simulation window
		window = QResizableMainWindow()
		self.mainWindow = SimulationWindow(window)

		# Setup the redirectioning of stdout to console
		self.console = Console()
		sys.stdout = self.console

		# Create the connexions
		self.console.printOccured.connect(self.mainWindow.printToConsole)

		# Show the window
		self.mainWindow.setup()
		window.show()

		configuration = self.mainWindow.readConfiguration()
		print(configuration)

		# Launch application
		# For more details: 
		# http://stackoverflow.com/questions/25075954/using-sys-exit-with-app-exec-in-pyqt
		sys.exit(app.exec_())


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