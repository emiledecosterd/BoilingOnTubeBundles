##	@package simulationWindow
#
#	Handles everything related to user input

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
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
		self.setupLists


	##	Fills the lists for all the comboboxes
	#	@param	None
	def setupLists(self):
		workingFluids = ['R134a', 'Propane', 'Ammonia']
		tubeMaterials = ['copper', 'aluminium', 'steel', 'other']
		layouts = ['Staggered', 'Inline']
		correlationsHTC = ['Mostinski', 'Cooper', 'Gorenflo']
		correlationsPD = ['Gaddis', 'Zukauskas']
		results = ['Th', 'Ph', 'Tc', 'Pc', 'xc', 'eps']


	##	Fills all the fields for a given configuration
	#	@param	configuration	A dictionary containing all the values for the fields
	#	@throw	error	An error with the name of the method and the exception message
	def setupInputs(self, configuration):

		if configuration:
			try:
				# Recover each dictionnary in the configuration
				opCond = configuration['opCond']
				geom = configuration['geom']
				flowInputs = configuration['flowInputs']
				
				# Fill all the fields
				# OpCond
				self.fluidTypeComboBox.setCurrentIndex(self.workingFluids.index(str(opCond['fluidType']))
				self.mfr_hLineEdit.setText(str(opCond['mfr_h']))
				self.mfr_cLineEdit.setText(str(opCond['mfr_c']))
				self.tubMatComboBox.setCurrentIndex(self.tubeMaterials.index(str(opCond['TubeMat'])))
				self.thermalConductivityLineEdit.setText(str(opCond['TubeThermalConductivity']))

				# Geom
				self.DsLineEdit.setText(str(geom['Ds']))
				self.DLineEdit.setText(str(geom['D']))
				self.NtSpinBox.setValue(int(geom['Nt']))
				self.Nt_ColSpinBox.setValue(int(geom['Nt_col']))
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
				self.chosenResultComboBox.setCurrentIndex(self.results.index(str(geom['choseResult'])))

				# flowInputs
				self.xcLineEdit.setText(str(flowInputs['xc_in']))
				self.paramCheckBox.setChecked(str(flowInputs['param']) is not None)
				Tc = flowInputs['Tc']
				Th = flowInputs['Th']
				Ph = flowInputs['Ph']
				self.TcCheckBox.setChecked(len(Tc)>1)
				self.ThCheckBox.setChecked(len(Th)>1)
				self.PhCheckBox.setChecked(len(Ph)>1)
				self.TcStartLineEdit.setText(str(Tc(0))) # Take the first element in the list
				self.TcEndLineEdit.setText(str(Tc(-1))) # Take the last element in the list
				self.ThStartLineEdit.setText(str(Th(0)))
				self.ThEndLineEdit.setText(str(Th(-1)))
				self.PhStartLineEdit.setText(str(Ph(0)))
				self.PhEndLineEdit.setText(str(Ph(-1)))
				self.paraSpinBox.setValue(max(len(Tc), len(Th), len(Ph))) # Number of elements

			except Exception as e:
				raise Error('simulationWindow.setupInputs()', e)


##	QResizableMainWindow
#
#	This class catches the resize event from the 'QMainWindow' class
#	and sends a signal
class QResizableMainWindow(QtWidgets.QMainWindow):

	resized = QtCore.pyqtSignal()

	def resizeEvent(self, resizeEvent):
		self.resized.emit()


