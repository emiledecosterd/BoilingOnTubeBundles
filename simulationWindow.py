##	@package simulationWindow
#
#	Handles everything related to user input

import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from numpy import linspace, array

from simulationWindowGUI import  Ui_MainWindow
from simulation import defaultConfiguration
from error import Error


##	SimulationWindow
#
#	The main window of the programm 
#	Handles user input 
#	Displays basic info to help create the simulation inputs
class SimulationWindow(Ui_MainWindow):

	# Lists containing all the fields in the comboboxes
	workingFluids = []
	tubeMaterials = []
	layouts = []
	correlationsHTC = []
	correlationsPD = []
	results = []

	##	The constructor
	#	@param	window	The reference to a QMainWindow object
	def __init__(self, window):

		Ui_MainWindow.__init__(self)
		self.window = window
		self.setupUi(window)


	##	Sets up the content and behaviour of the main window
	#	@param 	None
	def setup(self):
		self.setupLists()
		self.setupInputs(defaultConfiguration())


	##	Fills the lists for all the comboboxes
	#	@param	None
	def setupLists(self):
		self.workingFluids = ['R134a', 'Propane', 'Ammonia']
		self.tubeMaterials = ['copper', 'aluminium', 'steel', 'other']
		self.layouts = ['Staggered', 'Inline']
		self.correlationsHTC = ['Mostinski', 'Cooper', 'Gorenflo']
		self.correlationsPD = ['Gaddis', 'Zukauskas']
		self.results = ['Th', 'Ph', 'Tc', 'Pc', 'xc', 'eps']


	##	Fills all the fields for a given configuration
	#	@param	configuration	A dictionary containing all the values for the fields
	#	@throw	error	An error with the name of the method and the exception message
	def setupInputs(self, configuration):
		print('setupInputs')
		if configuration:
			try:
				# Recover each dictionnary in the configuration
				opCond = configuration['opCond']
				geom = configuration['geom']
				flowInputs = configuration['flowInputs']
				
				# Fill all the fields
				# OpCond
				self.fluidTypeComboBox.setCurrentIndex(self.workingFluids.index(str(opCond['FluidType'])))
				self.mfr_hLineEdit.setText(str(opCond['mfr_h']))
				self.mfr_cLineEdit.setText(str(opCond['mfr_c']))
				self.tubeMatComboBox.setCurrentIndex(self.tubeMaterials.index(str(opCond['TubeMat'])))
				self.tubeThermalConductivityLineEdit.setText(str(opCond['TubeThermalConductivity']))

				# Geom
				self.DsLineEdit.setText(str(geom['Ds']))
				self.DLineEdit.setText(str(geom['D']))
				self.NtSpinBox.setValue(int(geom['Nt']))
				self.Nt_colSpinBox.setValue(int(geom['Nt_col']))
				self.LLineEdit.setText(str(geom['L']))
				self.sLineEdit.setText(str(geom['s']))
				self.shLineEdit.setText(str(geom['sh']))
				self.tLineEdit.setText(str(geom['t']))
				self.layoutComboBox.setCurrentIndex(self.layouts.index(str(geom['layout'])))
				self.e_iLineEdit.setText(str(geom['e_i']))
				self.e_oLineEdit.setText(str(geom['e_o']))
				self.nSpinBox.setValue(int(geom['n']))
				self.corrComboBox.setCurrentIndex(self.correlationsHTC.index(str(geom['corr'])))
				self.corrPDComboBox.setCurrentIndex(self.correlationsPD.index(str(geom['corrPD'])))
				self.chosenResultComboBox.setCurrentIndex(self.results.index(str(geom['chosenResult'])))

				# flowInputs
				self.xcLineEdit.setText(str(flowInputs['xc_in']))
				self.paramCheckBox.setChecked(str(flowInputs['param']) is not None)
				Tc = flowInputs['Tc']
				Th = flowInputs['Th']
				Ph = flowInputs['Ph']
				self.TcCheckBox.setChecked(len(Tc)>1)
				self.ThCheckBox.setChecked(len(Th)>1)
				self.PhCheckBox.setChecked(len(Ph)>1)
				self.TcStartLineEdit.setText(str(Tc[0])) # Take the first element in the list
				self.TcEndLineEdit.setText(str(Tc[-1])) # Take the last element in the list
				self.ThStartLineEdit.setText(str(Th[0]))
				self.ThEndLineEdit.setText(str(Th[-1]))
				self.PhStartLineEdit.setText(str(Ph[0]))
				self.PhEndLineEdit.setText(str(Ph[-1]))
				self.paraSpinBox.setValue(max(len(Tc), len(Th), len(Ph))) # Number of elements

			except Exception as e:
				raise Error('simulationWindow.setupInputs()', e)

		else:
			print('No configuration passed')


	##	Reads all the fields in the GUI 
	#	@return	configuration A configuration dictionary
	def readConfiguration(self):
			print('Reading current fields')

			# Operating conditions fields
			opCond = {}
			opCond['FluidType'] = self.workingFluids[self.fluidTypeComboBox.currentIndex()]
			opCond['mfr_h'] = float(self.mfr_hLineEdit.text())
			opCond['mfr_c'] = float(self.mfr_cLineEdit.text())
			opCond['TubeMat'] = self.tubeMaterials[self.tubeMatComboBox.currentIndex()]
			opCond['TubeThermalConductivity'] = float(self.tubeThermalConductivityLineEdit.text())

			# Geometry fields
			geom = {}
			geom['Ds'] = float(self.DsLineEdit.text())
			geom['D'] = float(self.DLineEdit.text())
			geom['Nt'] = self.NtSpinBox.value()
			geom['Nt_col'] = self.Nt_colSpinBox.value()
			geom['L'] = float(self.LLineEdit.text())
			geom['s'] = float(self.sLineEdit.text())
			geom['sh'] = float(self.shLineEdit.text())
			geom['t'] = float(self.tLineEdit.text())
			geom['layout'] = self.layouts[self.layoutComboBox.currentIndex()]
			geom['e_i'] = float(self.e_iLineEdit.text())
			geom['e_o'] = float(self.e_oLineEdit.text())
			geom['n'] = self.nSpinBox.value()
			geom['corr'] = self.correlationsHTC[self.corrComboBox.currentIndex()]
			geom['corrPD'] = self.correlationsPD[self.corrPDComboBox.currentIndex()]
			geom['chosenResult'] = self.results[self.chosenResultComboBox.currentIndex()]

			# Flow inputs
			flowInputs = {}
			flowInputs['xc_in'] = float(self.xcLineEdit.text())

			# Calculate the lists
			Tc = []
			Th = []
			Ph = []
			if self.paramCheckBox.isChecked():
				val = self.paraSpinBox.value()
				TcStart = float(self.TcStartLineEdit.text())
				TcEnd = float(self.TcEndLineEdit.text())
				ThStart = float(self.ThStartLineEdit.text())
				ThEnd = float(self.ThEndLineEdit.text())
				PhStart = float(self.PhStartLineEdit.text())
				PhEnd = float(self.PhEndLineEdit.text())
				if TcEnd > TcStart:
					values = linspace(TcStart, TcEnd, val)
					Tc = values.tolist()
					flowInputs['param'] = 'Tc'
				elif ThEnd > ThStart:
					values = linspace(ThStart, ThEnd, val)
					Th = values.tolist()
					flowInputs['param'] = 'Th'
				elif PhEnd > PhStart:
					values = linspace(PhStart, PhEnd, val)
					Ph = values.tolist()
					flowInputs['param'] = 'Ph'

			else:
				Tc = [float(self.TcStartLineEdit.text())]
				Th = [float(self.ThStartLineEdit.text())]
				Ph = [float(self.PhStartLineEdit.text())]
				flowInputs['param'] = None

			flowInputs['Tc'] = Tc
			flowInputs['Th'] = Th
			flowInputs['Ph'] = Ph

			configuration = {'opCond': opCond, 'geom': geom, 'flowInputs': flowInputs}

			return configuration


	##	Print the given text to the console in the GUI
	#	@param 	text 	The text to print
	def printToConsole(self, text):
		strippedText = text.strip('\n')
		strippedText = strippedText.strip('\r')
		self.console.addItem(str(text))
		self.console.scrollToBottom()


##	QResizableMainWindow
#
#	This class catches the resize event from the 'QMainWindow' class
#	and sends a signal
class QResizableMainWindow(QtWidgets.QMainWindow):

	resized = QtCore.pyqtSignal()

	def resizeEvent(self, resizeEvent):
		self.resized.emit()


