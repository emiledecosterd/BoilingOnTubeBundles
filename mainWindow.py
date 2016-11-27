import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainWindowGUI import Ui_MainWindow

class MainWindow(Ui_MainWindow):

	# Signals for simulation
	startSimulation = pyqtSignal(dict)
	stopSimulation = pyqtSignal()

	def __init__(self, window, controller):

		# User interface setup
		Ui_MainWindow.__init__(self)
		self.setupUi(window)

		# Hold a reference to the controller 
		self.controller = controller

		# Current configuration for the simulation
		self.configuration = {} 


	# SETUP

	def setup(self):
		
		# Load the default setup (when the option for saving setups is added, load selected setup)
		''' configuration = readFile('defaultSetup.xml') '''

		configuration = {'opCond': None, 'flowInputs' : None, 'geom':None}
		self.setupRules()
		self.setupOperatingConditions(configuration['opCond'])
		self.setupGeometry(configuration['geom'])
		self.setupInputs(configuration['flowInputs'])
		self.setupInfos()


	def setupRules(self):
		# Define validators for each field
		self.mdot_c_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.mdot_c_lineEdit)) # Set the value as double
		self.mdot_h_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.mdot_h_lineEdit)) # Set the value as double
		#self.Nt_lineEdit.setValidator(QRegExpValidator(QRegExp("[0-9]*"))) # Set the value as int
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
		self.Tc_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Tc_lineEdit)) # Set the value as double
		self.Th_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Th_lineEdit)) # Set the value as double
		self.Pc_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Pc_lineEdit)) # Set the value as double
		self.Ph_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.Ph_lineEdit)) # Set the value as double
		self.xc_lineEdit.setValidator(QRegExpValidator(
			QRegExp("[0-9]*\.?[0-9]+([eE][-]?[0-9]+)"),self.xc_lineEdit)) # Set the value as double

		# Buttons
		self.run_button.clicked.connect(self.on_run)
		self.save_button.clicked.connect(self.on_saveConfiguration)
		self.load_button.clicked.connect(self.on_loadConfiguration)

		# Listen to signals sent by some fields
		self.Nt_spinBox.valueChanged.connect(self.on_Nt_changed)
		self.n_spinBox.valueChanged.connect(self.on_n_changed)


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
			geom = infos
		else:

			# Put default values
			geom = {}

			geom['Nt'] = 3
			geom['Nt_col'] = 2
			geom['L'] = 1.0
			geom['n'] = 6
			geom['s'] = 23.81e-3
			geom['D'] = 19.05e-3
			geom['e_i'] = 2e-6
			geom['e_o'] = 2e-6
			geom['t'] = 2e-3
			geom['corr'] = 'Mostinski'


		# Keep a reference to the current setup
		self.configuration['geom'] = geom
		# Display changes
		self.reloadGeometry()


	def reloadGeometry(self):
	
		setup = self.configuration['geom']

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

		self.controller.redrawSchema(setup)


	def setupOperatingConditions(self, infos):

		if infos is not None:
			self.configuration['opCond'] = infos
		else:

			# Put default values
			opCond = {}

			opCond['FluidType'] = 'R134a'
			opCond['mdot_c'] = 27.8
			opCond['mdot_h'] = 103.0 # Need to guess it
			opCond['TubeMat'] = 'steel'
			opCond['TubeThermalConductivity']= 400

			self.configuration['opCond'] = opCond

		## Fill the fields in the GUI
		opCond = self.configuration['opCond']

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
		self.tubeThermalConductivity_lineEdit.setText(str(opCond['TubeThermalConductivity']))


	def setupInputs(self, infos):

		if infos is not None:
			self.configuration['flowInputs'] = infos
		else:

			flowInputs = {}

			flowInputs['Tc_in'] = 0.0 + 273.15
			flowInputs['Th_in'] = 10+ 273.15
			flowInputs['Pc_in'] = 1e5
			flowInputs['Ph_in'] = 1e5
			flowInputs['xc_in'] = 0.13

			self.configuration['flowInputs'] = flowInputs

		inputs = self.configuration['flowInputs']

		self.Tc_lineEdit.setText(str(inputs['Tc_in']))
		self.Th_lineEdit.setText(str(inputs['Th_in']))
		self.Pc_lineEdit.setText(str(inputs['Pc_in']))
		self.Ph_lineEdit.setText(str(inputs['Ph_in']))
		self.xc_lineEdit.setText(str(inputs['xc_in']))


	# EVENTS

	def updateConfiguration(self):

		# Update the configuration according to the values given by the user
		self.configuration['flowInputs']['Tc_in'] = float(self.Tc_lineEdit.text)
		self.configuration['flowInputs']['Th_in'] = float(self.Th_lineEdit.text)
		self.configuration['flowInputs']['Pc_in'] = float(self.Pc_lineEdit.text)
		self.configuration['flowInputs']['Ph_in'] = float(self.Ph_lineEdit.text)
		self.configuration['flowInputs']['xc_in'] = float(self.xc_lineEdit.text)
			
		self.configuration['geom']['Nt'] = self.Nt_spinBox.value()
		self.configuration['geom']['Nt_col'] = self.Nt_col_spinBox.value()
		self.configuration['geom']['L'] = float(self.L_lineEdit.text)
		self.configuration['geom']['n'] = self.n_spinBox.value()
		self.configuration['geom']['s'] = float(self.s_lineEdit.text)
		self.configuration['geom']['D'] = float(self.D_lineEdit.text)
		self.configuration['geom']['e_o'] = float(self.e_o_lineEdit.text)
		self.configuration['geom']['e_i'] = float(self.e_i_lineEdit.text)
		self.configuration['geom']['t'] = float(self.t_lineEdit.text)
		self.configuration['geom']['corr'] = self.corr_comboBox.currentText

		self.configuration['opCond']['FluidType'] = self.fluid_comboBox.text
		self.configuration['opCond']['TubeMat'] = self.tubeMaterial_comboBox.currentText 
		self.configuration['opCond']['mdot_c'] = float(self.mdot_c_lineEdit.text) 
		self.configuration['opCond']['mdot_h'] = float(self.mdot_h_lineEdit.text)
		self.configuration['opCond']['TubeThermalConductivity'] = float(self.tubeThermalConductivity_lineEdit.text) 


	def on_saveConfiguration(self):

		filename = 'default'

		# Verify filename
		if self.configuration_lineEdit.text is not None:
			filename = self.configuration_lineEdit.text

		# Save the file
		self.controller.saveConfiguration(filename, self.configuration)


	def on_loadConfiguration(self):

		self.controller.loadConfiguration()


	# Start simulation
	def on_run(self):

		if self.running == True:
			self.run_button.setText('Run')
			self.simulation_progressBar.setProperty("visible", False)
			self.simulation_progressBar.setProperty("value", 0)
			self.running = False

			self.stopSimulation.emit()

		else:
			self.running = True # Remember that we are running a simulation
			self.run_button.setText('Stop')
			self.simulation_progressBar.setProperty("visible", True)

			self.startSimulation.emit(self.configuration)

	# Update progress bar
	def on_updateProgress(self,progress):
		self.simulation_progressBar.setProperty("value", progress)

	# Number of pipes changed
	def on_Nt_changed(self):

		self.configuration['geom']['Nt'] = self.Nt_spinBox.value()
		self.reloadGeometry()

	# Number of cells changed
	def on_n_changed(self):

		self.configuration['geom']['n'] = self.n_spinBox.value()
		self.reloadGeometry()

		

