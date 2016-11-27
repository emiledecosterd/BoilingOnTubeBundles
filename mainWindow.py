import sys
import math

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainWindowGUI import Ui_MainWindow

class MainWindow(Ui_MainWindow):

	# Configuration¨
	opCond = None
	geom = None
	flowInputs = None
	currentParam = 'None'

	# Mass flow
	currentMassFlow_c = 'mfr'
	currentMassFlow_h = 'mfr'

	# Signals for simulation
	startSimulation = pyqtSignal(dict)
	stopSimulation = pyqtSignal()

	def __init__(self, window, controller):

		# User interface setup
		Ui_MainWindow.__init__(self)
		self.setupUi(window)


	# SETUP

	def setup(self):
		
		# Load the default setup (when the option for saving setups is added, load selected setup)
		''' configuration = readFile('defaultSetup.xml') '''

		self.setupOperatingConditions(None)
		self.setupGeometry(None)
		self.setupInputs(None)
		self.setupInfos()
		self.setupRules()
		self.on_update_param('None')

	def setupRules(self):

		# OpCond validators
		self.mdot_c_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.mdot_c_lineEdit)) # Set the value as double
		self.mdot_h_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.mdot_h_lineEdit)) # Set the value as double
		self.mfr_c_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.mfr_c_lineEdit)) # Set the value as double
		self.mfr_h_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.mfr_h_lineEdit)) # Set the value as double

		# Geometry validators
		self.L_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"), self.L_lineEdit)) # Set value as double
		self.s_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.s_lineEdit)) # Set the value as double
		self.D_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.D_lineEdit)) # Set the value as double
		self.e_o_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.e_o_lineEdit)) # Set the value as double
		self.e_i_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.e_i_lineEdit)) # Set the value as double
		self.t_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.t_lineEdit)) # Set the value as double
		self.sq_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.sq_lineEdit)) # Set the value as double
		self.sl_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.sl_lineEdit)) # Set the value as double

		# Flow inputs validators
		self.Tc_start_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Tc_start_lineEdit)) # Set the value as double
		self.Tc_end_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Tc_end_lineEdit)) # Set the value as double
		self.Th_start_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Th_start_lineEdit)) # Set the value as double
		self.Th_end_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Th_end_lineEdit)) # Set the value as double
		self.Ph_start_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Ph_start_lineEdit)) # Set the value as double
		self.Ph_end_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Ph_end_lineEdit)) # Set the value as double
		self.xc_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.xc_lineEdit)) # Set the value as double

		# Buttons
		self.run_button.clicked.connect(self.on_run)
		self.save_button.clicked.connect(self.on_saveConfiguration)
		self.load_button.clicked.connect(self.on_loadConfiguration)

		# Listen to signals sent by some fields
		self.Nt_spinBox.valueChanged.connect(self.on_Nt_changed)
		self.Nt_spinBox.valueChanged.connect(lambda: self.on_opCond_changed(None))
		self.Nt_col_spinBox.valueChanged.connect(lambda: self.on_opCond_changed(None))
		self.D_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed(None))
		self.t_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed(None))
		self.s_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed(None))
		self.L_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed(None))
		self.n_spinBox.valueChanged.connect(self.on_n_changed)
		self.mfr_c_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed('mfr_c'))
		self.mfr_h_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed('mfr_h'))
		self.mdot_c_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed('mdot_c'))
		self.mdot_h_lineEdit.editingFinished.connect(lambda: self.on_opCond_changed('mdot_h'))
		self.Tc_checkBox.clicked.connect(lambda: self.on_update_param('Tc'))
		self.Th_checkBox.clicked.connect(lambda: self.on_update_param('Th'))
		self.Ph_checkBox.clicked.connect(lambda: self.on_update_param('Ph'))


	def setupInfos(self):

		self.running = False
		self.simulationProgress = 0;

		# Filename
		self.configuration_lineEdit.setText('default')

		# Progress bar
		self.simulation_progressBar.setProperty("minimum", 0)
		self.simulation_progressBar.setProperty("maximum", 100)
		self.simulation_progressBar.setProperty("value", 0)
		self.simulation_progressBar.setProperty("visible", False)


	def setupGeometry(self, infos):

		if infos is not None:
			self.geom = infos
		else:

			# Put default values
			self.geom = {}

			self.geom['Nt'] = 3
			self.geom['Nt_col'] = 2
			self.geom['L'] = 1.0
			self.geom['n'] = 6
			self.geom['s'] = 23.81e-3
			self.geom['D'] = 19.05e-3
			self.geom['e_i'] = 2e-6
			self.geom['e_o'] = 2e-6
			self.geom['t'] = 2e-3
			self.geom['corr'] = 'Mostinski'
			self.geom['corrPD'] = 'Gaddis'
			self.geom['layout'] = 'Staggered'
			self.geom['sq'] = 150e-3
			self.geom['sl'] = 150e-3
			self.geom['N'] = self.geom['Nt']*self.geom['Nt_col']


		# Display changes
		self.reloadGeometry()


	def reloadGeometry(self):
	
		setup = self.geom

		self.Nt_spinBox.setValue(int(setup['Nt']))
		self.Nt_col_spinBox.setValue(int(setup['Nt_col']))
		self.L_lineEdit.setText(str(setup['L']))
		self.n_spinBox.setValue(int(setup['n']))
		self.s_lineEdit.setText(str(setup['s']))
		self.D_lineEdit.setText(str(setup['D']))
		self.e_o_lineEdit.setText(str(setup['e_o']))
		self.e_i_lineEdit.setText(str(setup['e_i']))
		self.t_lineEdit.setText(str(setup['t']))
		self.corr_comboBox.currentText = setup['corr']
		self.corrPD_comboBox.currentText = setup['corrPD']
		self.sq_lineEdit.setText(str(setup['sq']))
		self.sl_lineEdit.setText(str(setup['sl']))

		# Send signal to redraw geometry


	def setupOperatingConditions(self, infos):

		if infos is not None:
			self.opCond = infos
		else:

			# Put default values
			self.opCond = {}
			self.opCond['FluidType'] = 'R134a'
			self.opCond['mdot_c'] = 27.8
			self.opCond['mdot_h'] = 103.0 # Need to guess it
			self.opCond['mfr_c'] = 5.3
			self.opCond['mfr_h'] = 15 #mfr_hGuess

			self.opCond['TubeMat'] = 'steel'
			self.opCond['TubeThermalConductivity']= 400

		## Fill the fields in the GUI
		opCond = self.opCond

		if opCond['FluidType'] == 'R134a':
			self.fluid_comboBox.setCurrentIndex(0)
		elif opCond['FluidType'] == 'Ammonia':
			self.fluid_comboBox.setCurrentIndex(1)
		elif opCond['FluidType'] == 'Propane':
			self.fluid_comboBox.setCurrentIndex(2)

		if opCond['TubeMat'] == 'copper':
			self.tubeMaterial_comboBox.setCurrentIndex(0)
		elif opCond['TubeMat'] == 'aluminium':
			self.tubeMaterial_comboBox.setCurrentIndex(1)
		elif opCond['TubeMat'] == 'steel':
			self.tubeMaterial_comboBox.setCurrentIndex(2)

		self.mdot_c_lineEdit.setText(str(opCond['mdot_c']))
		self.mdot_h_lineEdit.setText(str(opCond['mdot_h']))
		self.mfr_c_lineEdit.setText(str(opCond['mfr_c']))
		self.mfr_h_lineEdit.setText(str(opCond['mfr_h']))
		self.tubeThermalConductivity_lineEdit.setText(str(opCond['TubeThermalConductivity']))


	def setupInputs(self, infos):

		if infos is not None:
			self.flowInputs = infos
		else:

			self.flowInputs = {}

			self.flowInputs['Tc_start'] = 0.0 + 273.15
			self.flowInputs['Tc_end'] = 10.0 + 273.15
			self.flowInputs['Th_start'] = 10+ 273.15
			self.flowInputs['Th_end'] = 20+ 273.15
			self.flowInputs['Ph_start'] = 1e5
			self.flowInputs['Ph_end'] = 100e5
			self.flowInputs['xc_in'] = 0.13
			self.flowInputs['steps'] = 100

		self.nVal_spinBox.setValue(self.flowInputs['steps'])
		self.Tc_start_lineEdit.setText(str(self.flowInputs['Tc_start']))
		self.Tc_end_lineEdit.setText(str(self.flowInputs['Tc_end']))
		self.Th_start_lineEdit.setText(str(self.flowInputs['Th_start']))
		self.Th_end_lineEdit.setText(str(self.flowInputs['Th_end']))
		self.Ph_start_lineEdit.setText(str(self.flowInputs['Ph_start']))
		self.Ph_end_lineEdit.setText(str(self.flowInputs['Ph_end']))
		self.xc_lineEdit.setText(str(self.flowInputs['xc_in']))


	# EVENTS

	def updateConfiguration(self):

		# Update the configuration according to the values given by the user
		self.flowInputs['Tc_start'] = float(self.Tc_start_lineEdit.text())
		self.flowInputs['Tc_end'] = float(self.Tc_end_lineEdit.text())
		self.flowInputs['Th_start'] = float(self.Th_start_lineEdit.text())
		self.flowInputs['Th_end'] = float(self.Th_end_lineEdit.text())
		self.flowInputs['Ph_start'] = float(self.Ph_start_lineEdit.text())
		self.flowInputs['Ph_end'] = float(self.Ph_end_lineEdit.text())
		self.flowInputs['xc_in'] = float(self.xc_lineEdit.text())
		self.flowInputs['steps']= self.nVal_spinBox.value()
			
		self.geom['Nt'] = self.Nt_spinBox.value()
		self.geom['Nt_col'] = self.Nt_col_spinBox.value()
		self.geom['L'] = float(self.L_lineEdit.text())
		self.geom['n'] = self.n_spinBox.value()
		self.geom['s'] = float(self.s_lineEdit.text())
		self.geom['D'] = float(self.D_lineEdit.text())
		self.geom['e_o'] = float(self.e_o_lineEdit.text())
		self.geom['e_i'] = float(self.e_i_lineEdit.text())
		self.geom['t'] = float(self.t_lineEdit.text())
		self.geom['corr'] = self.corr_comboBox.currentText
		self.geom['corrPD'] = self.corrPD_comboBox.currentText
		self.geom['sq'] = self.sq_lineEdit.text()
		self.geom['sl'] = self.sl_lineEdit.text()

		self.opCond['FluidType'] = self.fluid_comboBox.currentText
		self.opCond['TubeMat'] = self.tubeMaterial_comboBox.currentText 
		self.opCond['mdot_c'] = float(self.mdot_c_lineEdit.text()) 
		self.opCond['mdot_h'] = float(self.mdot_h_lineEdit.text())
		self.opCond['mfr_c'] = float(self.mfr_c_lineEdit.text())
		self.opCond['mfr_h'] = float(self.mfr_h_lineEdit.text())
		self.opCond['TubeThermalConductivity'] = float(self.tubeThermalConductivity_lineEdit.text()) 
		


	def on_saveConfiguration(self):

		filename = 'default' # Todays date

		# Verify filename
		if self.configuration_lineEdit.text() is not None:
			filename = self.configuration_lineEdit.text()

		# Save the file
		# Send signal with configuration


	def on_loadConfiguration(self):

		# Send signal with reference to self

		print('Send signal')


	# Start simulation
	def on_run(self):

		self.simulation_progressBar.setProperty("visible", True)
		configuration = {'opCond': self.opCond, 'geom': self.geom, 'flowInputs':self.flowInputs}
		self.startSimulation.emit(configuration)


	def on_update_param(self, param):

		changed = False

		if param == 'Tc':
			if self.Tc_checkBox.isChecked():
				self.currentParam = 'Tc'
				self.Tc_end_lineEdit.setEnabled(True)
				self.Tc_checkBox.setChecked(True)
				self.Th_end_lineEdit.setEnabled(False)
				self.Th_checkBox.setChecked(False)
				self.Ph_end_lineEdit.setEnabled(False)
				self.Ph_checkBox.setChecked(False)
				self.nVal_spinBox.setEnabled(True)
			else:
				self.currentParam = 'None'
			
		elif param == 'Th':
			if self.Th_checkBox.isChecked():
				self.currentParam = 'Th'
				self.Tc_end_lineEdit.setEnabled(False)
				self.Tc_checkBox.setChecked(False)
				self.Th_end_lineEdit.setEnabled(True)
				self.Th_checkBox.setChecked(True)
				self.Ph_end_lineEdit.setEnabled(False)
				self.Ph_checkBox.setChecked(False)
				self.nVal_spinBox.setEnabled(True)
			else:
				self.currentParam = 'None'

		elif param == 'Ph':
			if self.Ph_checkBox.isChecked():
				self.currentParam = 'Ph'
				self.Tc_end_lineEdit.setEnabled(False)
				self.Tc_checkBox.setChecked(False)
				self.Th_end_lineEdit.setEnabled(False)
				self.Th_checkBox.setChecked(False)
				self.Ph_end_lineEdit.setEnabled(True)
				self.Ph_checkBox.setChecked(True)
				self.nVal_spinBox.setEnabled(True)
			else:
				self.currentParam = 'None'

		if self.currentParam == 'None':
			self.Tc_end_lineEdit.setEnabled(False)
			self.Tc_checkBox.setChecked(False)
			self.Th_end_lineEdit.setEnabled(False)
			self.Th_checkBox.setChecked(False)
			self.Ph_end_lineEdit.setEnabled(False)
			self.Ph_checkBox.setChecked(False)
			self.nVal_spinBox.setEnabled(False)

		print(self.currentParam)


	# Update progress bar
	def on_updateProgress(self,progress):
		self.simulation_progressBar.setProperty("value", progress)

	# Number of pipes changed
	def on_Nt_changed(self):

		self.geom['Nt'] = self.Nt_spinBox.value()
		self.reloadGeometry()

	# Number of cells changed
	def on_n_changed(self):

		self.geom['n'] = self.n_spinBox.value()
		self.reloadGeometry()


	# An operating condition concerning the mass flow rate changed
	def on_opCond_changed(self, flowRate):

		print('opCond changed')
		geom = self.geom
		opCond = self.opCond

		# If flowrate is None, the call does not come from the "editingFinished" signal 
		# but because some geometry field changed
		if flowRate is None:
			if self.currentMassFlow_c == 'mfr':
				self.on_opCond_changed('mfr_c')
			elif self.currentMassFlow_c == 'mdot':
				self.on_opCond_changed('mdot_c')

			if self.currentMassFlow_h == 'mfr':
				self.on_opCond_changed('mfr_h')
			elif self.currentMassFlow_h == 'mdot':
				self.on_opCond_changed('mdot_h')

		# Save the values of the GUI in instance variables
		self.updateConfiguration();

		# Calculate conversion factors
		factor_h = geom['Nt']*geom['Nt_col']*math.pi*0.25*(geom['D']-2*geom['t'])**2
		factor_c = (geom['Nt_col']*geom['s']*geom['L'])

		if flowRate == 'mfr_c':

			print('mfr_c changed')
			# Remember we want to change mfr and not mdot
			self.currentMassFlow_c = 'mfr'

			# Change mdot_c accordingly and display changes
			opCond['mdot_c'] = opCond['mfr_c']/factor_c
			self.mdot_c_lineEdit.setText(str(opCond['mdot_c']))

		elif flowRate == 'mfr_h':

			print('mfr_h changed')
			# Remember we want to change mfr and not mdot
			self.currentMassFlow_h = 'mfr'

			# Change mdot_h accordingly
			opCond['mdot_h'] = opCond['mfr_h']/factor_h
			self.mdot_h_lineEdit.setText(str(opCond['mdot_h']))

		elif flowRate == 'mdot_c':

			print('mdot_c changed')
			# Remember we want to change mdot and not mfr
			self.currentMassFlow_c = 'mdot'

			# Change mfr_c accordingly
			opCond['mfr_c'] = opCond['mdot_c']*factor_c
			self.mfr_c_lineEdit.setText(str(opCond['mfr_c']))

		elif flowRate == 'mdot_h':

			print('mdot_h changed')
			# Remember we want to change mdot and not mfr
			self.currentMassFlow_h = 'mdot'

			# Change mfr_c accordingly
			opCond['mfr_h'] = opCond['mdot_h']*factor_h
			self.mfr_h_lineEdit.setText(str(opCond['mfr_h']))


	def on_check_corr(self):

			print('check')









		

