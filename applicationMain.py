##	@package applicationMain
#
#	The link between GUI, Simulation and PostProcessing

import sys

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

		# Create the connexions
		self.console.printOccured.connect(self.mainWindow.printToConsole)
		self.mainWindow.changesOccured.connect(self.resetResults)
		self.mainWindow.changesOccured.connect(self.updatePlots)
		self.mainWindow.chosenResultChanged.connect(self.updatePlots)
		self.mainWindow.graphicsView.clicked.connect(self.togglePlotter)
		self.mainWindow.showPlotsButton.clicked.connect(self.showPlots)
		window.resized.connect(self.updatePlots)

		# Show the window
		window.show()

		# Launch application
		# For more details: 
		# http://stackoverflow.com/questions/25075954/using-sys-exit-with-app-exec-in-pyqt
		sys.exit(app.exec_())


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
			print('Error plotting the tube bundles. \nCheck your parameters (perhaps you put something to 0)')


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