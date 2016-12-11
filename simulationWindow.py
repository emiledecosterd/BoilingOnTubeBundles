##	@package simulationWindow
#
#	Handles everything related to user input

import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from numpy import linspace, array
import math

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

	# Signals
	changesOccured = QtCore.pyqtSignal()
	chosenResultChanged = QtCore.pyqtSignal(str)

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
		self.setupConnections()
		self.setupRules()

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
				print(flowInputs['param'])
				self.paramCheckBox.setChecked(flowInputs['param'] is not None )
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

			# Gray out fields depending on configuration
			self.checkTubeMaterial()
			self.checkCorrPD()
			self.checkParam()

		else:
			print('No configuration passed')


	##	setupConnections()
	#	Sets up the connexions and signals
	#	@param None
	def setupConnections(self):

		# Everything that could alter the plot
		self.DsLineEdit.editingFinished.connect(self.inputsChanged)
		self.DLineEdit.editingFinished.connect(self.inputsChanged)
		self.NtSpinBox.valueChanged.connect(self.inputsChanged)
		self.Nt_colSpinBox.valueChanged.connect(self.inputsChanged)
		self.sLineEdit.editingFinished.connect(self.inputsChanged)
		self.shLineEdit.editingFinished.connect(self.inputsChanged)
		self.layoutComboBox.currentIndexChanged.connect(self.inputsChanged)
		self.nSpinBox.valueChanged.connect(self.inputsChanged)

		# Everything that need verification
		self.tubeMatComboBox.currentIndexChanged.connect(self.checkTubeMaterial)
		self.corrPDComboBox.currentIndexChanged.connect(self.checkCorrPD)
		self.paramCheckBox.stateChanged.connect(self.checkParam)
		self.TcCheckBox.stateChanged.connect(self.checkParam)
		self.ThCheckBox.stateChanged.connect(self.checkParam)
		self.PhCheckBox.stateChanged.connect(self.checkParam)

		# For the plots
		self.chosenResultComboBox.currentIndexChanged.connect(self.sendChosenResult)


	##	setupRules()
	#	Sets up the validators and other formatting or behavioural rules
	#	@param 	None
	def setupRules(self):
		self.console.setReadOnly(False)

		# Validators
		validator = QtGui.QDoubleValidator(0,1e9,4)
		validator.setLocale(QtCore.QLocale('Suisse'))
		self.mfr_hLineEdit.setValidator(validator)
		self.mfr_cLineEdit.setValidator(validator)
		self.tubeThermalConductivityLineEdit.setValidator(validator)
		self.DsLineEdit.setValidator(validator)
		self.DLineEdit.setValidator(validator)
		self.LLineEdit.setValidator(validator)
		self.sLineEdit.setValidator(validator)
		self.shLineEdit.setValidator(validator)
		self.tLineEdit.setValidator(validator)
		self.e_iLineEdit.setValidator(validator)
		self.e_oLineEdit.setValidator(validator)
		self.xcLineEdit.setValidator(validator)
		self.TcStartLineEdit.setValidator(validator)
		self.TcEndLineEdit.setValidator(validator)
		self.ThStartLineEdit.setValidator(validator)
		self.ThEndLineEdit.setValidator(validator)
		self.PhStartLineEdit.setValidator(validator)
		self.PhEndLineEdit.setValidator(validator)



	##	Bridge between the signals from the fields and the maincontroller
	def inputsChanged(self):
		print('Input changed')
		print(self.readConfiguration())
		self.changesOccured.emit()

	##	Called whenever the user chooses another field to display
	def sendChosenResult(self):
		print('ChosenResult changed')
		result = self.results[self.chosenResultComboBox.currentIndex()]
		self.chosenResultChanged.emit(result)


	##	Check if the tube material is defined. If so, disable the thermal
	#	conductivity line edit (for a given material, this k is fixed)
	#	@param 	None
	def checkTubeMaterial(self):
		if self.tubeMaterials[self.tubeMatComboBox.currentIndex()] == 'other':
			self.tubeThermalConductivityLineEdit.setEnabled(True)
		else:
			self.tubeThermalConductivityLineEdit.setEnabled(False)


	##	Checks if some inputs have to be enabled depending on the correlation
	#	chosen for the pressure drop
	#	@param 	None
	def checkCorrPD(self):
		if self.correlationsPD[self.corrPDComboBox.currentIndex()] == 'Gaddis':
			self.shLineEdit.setEnabled(True)
			self.layoutComboBox.setEnabled(True)
		else:
			self.shLineEdit.setEnabled(False)
			self.layoutComboBox.setEnabled(False)


	currentCheckBox = None

	##	Checks which fields have to be enabled or disabled depending on the 
	#	user input for the parametric simulation
	#	@param 	None
	def checkParam(self):

		checkBoxes = [self.TcCheckBox, self.ThCheckBox, self.PhCheckBox]
		lineEdits = [self.TcEndLineEdit, self.ThEndLineEdit, self.PhEndLineEdit]
		checkedIndex = None;
		if self.paramCheckBox.isChecked():
			self.paraSpinBox.setEnabled(True)
			for i in range(0, len(checkBoxes)):
				checkBoxes[i].setEnabled(True)
				if self.currentCheckBox is not None:
					if self.currentCheckBox == checkBoxes[i]:
						checkBoxes[i].setChecked(False)
						self.currentCheckBox = None
				if checkBoxes[i].isChecked():
					checkedIndex = i
					for j in range(0,len(checkBoxes)):
						if i!=j:
							lineEdits[j].setEnabled(False)
			if checkedIndex is not None:
				self.currentCheckBox = checkBoxes[checkedIndex]
				lineEdits[checkedIndex].setEnabled(True)
		else:
			self.paraSpinBox.setEnabled(False)
			for i in range(0, len(checkBoxes)):
				checkBoxes[i].setEnabled(False)
				checkBoxes[i].setChecked(False)
				lineEdits[i].setEnabled(False)


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
			geom['N'] = geom['Nt']*geom['Nt_col']

			# Calculate mdotdot
			opCond['mdot_h'] = opCond['mfr_h']/(geom['N']*math.pi*0.25*(geom['D']-2*geom['t'])**2)
			opCond['mdot_c'] = opCond['mfr_c']/(geom['Nt_col']*geom['s']*geom['L'])

			# Flow inputs
			flowInputs = {}
			flowInputs['xc_in'] = float(self.xcLineEdit.text())

			# Calculate the lists
			TcStart = float(self.TcStartLineEdit.text())
			ThStart = float(self.ThStartLineEdit.text())
			PhStart = float(self.PhStartLineEdit.text())
			Tc = [TcStart]
			Th = [ThStart]
			Ph = [PhStart]
			if self.paramCheckBox.isChecked():
				val = self.paraSpinBox.value()
				TcEnd = float(self.TcEndLineEdit.text())
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
		if text != '\n':
			text = '>>> ' + text
		cursor = self.console.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.console.setTextCursor(cursor)
		self.console.ensureCursorVisible()


##	QResizableMainWindow
#
#	This class catches the resize event from the 'QMainWindow' class
#	and sends a signal
class QResizableMainWindow(QtWidgets.QMainWindow):

	resized = QtCore.pyqtSignal()

	def resizeEvent(self, resizeEvent):
		self.resized.emit()


