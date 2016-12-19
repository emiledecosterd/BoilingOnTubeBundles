##	@package resultsDialog
#	Results display, plots
#
#	Dialog window used to display all the plots and the heat transfered in the simulation

# Package for the results dialog

import sys, os
import tkinter as tk
from tkinter import filedialog

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from resultsDialogGUI import Ui_Dialog
import matplotlib.pyplot as plt
import pickle


##	ResultsDialog
#	Plots and results manager
class ResultsDialog(Ui_Dialog):
	
	##	Default constructor
	#	@param dialog QtWidgets.QDialog
	def __init__(self, dialog, config):
		Ui_Dialog.__init__(self) 
		self.setupUi(dialog) 

		self.dialog = dialog

		# Initialize GridLayout
		self.gridLayout = QtWidgets.QGridLayout()
		self.verticalLayout_2.addLayout(self.gridLayout)

		# Global variables
		self.directoryName = config['filename']

		# Setup
		self.setupLists()
		self.lineEditCapacity.setReadOnly(True)

		# Setup data
		self.setupData()

		# Setup signals
		self.comboBoxPlotView.currentIndexChanged.connect(self.updatePlotLayout)
		self.pushButton.clicked.connect(self.changeOutput)

		# Initialize layout
		# self.comboBoxPlotView.setCurrentIndex(0)
		self.updatePlotLayout()

	

	#	SETUP METHODS

	def setupData(self):
		# Load images 
		self.loadFigures()
		self.loadData()


	def setupLists(self):

		# Setup widgets lists
		self.widgetsList = []
		self.layoutHorList = []
		self.layoutVertList = []
		self.comboBoxList = []
		self.graphicsViewList = []
		self.figuresList = []

		# Setup Plot Label (Pretty)
		self.prettyPlotName = ['Plot Average x wf', 'Plot Tw', 'Plot Pw', 'Plot Twf', 'Plot Pwf', 'Plot x wf', 'Plot eps']
		self.plotName = ['avg_xc', 'T_w','P_w','T_wf','P_wf','x_wf', 'eps']

		# Setup Plot Layout indexes
		self.nPlots = [1, 4, 6]
		self.resizeWidthRatio = [1, 2, 3]
		self.resizeHeightRatio = [1, 2, 2]

	def loadFigures(self):
		self.figuresList = []
		for key in self.plotName:
			with open(self.directoryName + '/mplt/plot_' + key, 'rb') as plotPath:
				self.figuresList.append(pickle.load(plotPath))

		# with open(self.directoryName + '/mplt/plot_avg_xc', 'rb') as plotPath:
		# 		self.figuresList.append(pickle.load(plotPath))
		
	#	PLOTS METHODS

	def addNewPlot(self, row, column):

		# Create new objects
		self.widgetsList.append(QtWidgets.QWidget(self.plotWidget))
		self.widgetsList[-1].setMinimumSize(400,300)
		self.layoutVertList.append(QtWidgets.QVBoxLayout(self.widgetsList[-1]))

		# self.layoutVertList.append(QtWidgets.QVBoxLayout(self.plotWidget))
		self.layoutHorList.append(QtWidgets.QHBoxLayout())
		spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.layoutHorList[-1].addItem(spacer)
		# self.comboBoxList.append(QtWidgets.QComboBox(self.plotWidget)) 
		self.comboBoxList.append(QtWidgets.QComboBox(self.widgetsList[-1])) 


		self.layoutHorList[-1].addWidget(self.comboBoxList[-1])
		self.layoutVertList[-1].addLayout(self.layoutHorList[-1])

		# self.gridLayout.addLayout(self.layoutVertList[-1], row, column)
		self.gridLayout.addWidget(self.widgetsList[-1], row, column)


		self.gridLayout.setRowStretch(row, 0)
		self.gridLayout.setColumnStretch(column, 0)
		

		# Setup Combobox
		self.comboBoxList[-1].setMinimumSize(QtCore.QSize(190,0))
		self.comboBoxList[-1].setMaximumSize(QtCore.QSize(190,16777215))
		for item in range(len(self.prettyPlotName)) :
			self.comboBoxList[-1].addItem('')
			self.comboBoxList[-1].setItemText(item, self.prettyPlotName[item])
		self.comboBoxList[-1].currentIndexChanged.connect(self.updatePlots)
		

	def updatePlotLayout(self):
			self.layoutIndex = self.comboBoxPlotView.currentIndex()			

			# Clear all plots and lists
			for i in range(len(self.graphicsViewList)):
				self.widgetsList[i].setParent(None)
				self.layoutHorList[i].setParent(None)
				self.layoutVertList[i].setParent(None)
				self.comboBoxList[i].setParent(None)
				self.graphicsViewList[i].setParent(None)
			self.widgetsList = []
			self.layoutHorList = []
			self.layoutVertList = []
			self.comboBoxList = []
			self.graphicsViewList = []

			# Setup new GridLayout
			self.gridLayout.setParent(None)
			del self.gridLayout
			self.gridLayout = QtWidgets.QGridLayout()
			self.verticalLayout_2.addLayout(self.gridLayout)

			# Number of plots to displays
			nPlots = self.nPlots[self.layoutIndex]

			# Add plot to the gridlayout
			if nPlots == 1:
				self.addNewPlot(0,0)
				oldState = self.comboBoxList[-1].blockSignals(True)
				self.comboBoxList[-1].setCurrentIndex(0)
				self.comboBoxList[-1].blockSignals(oldState);
			for i in range(2):
				for j in range(round(nPlots/2)):
					self.addNewPlot(i,j)
					oldState = self.comboBoxList[-1].blockSignals(True)
					self.comboBoxList[-1].setCurrentIndex(j+(nPlots/2)*i)
					self.comboBoxList[-1].blockSignals(oldState);

			# Plot everything
			self.updatePlots()
				

	def updatePlots(self):
		print('total size')
		print([self.plotWidget.width(), self.plotWidget.height()])

		# Get the size of the window
		totalWidth =  self.plotWidget.width()
		totalHeight =  self.plotWidget.height()

		# Reset all plots
		for i in range(len(self.graphicsViewList)):
			self.graphicsViewList[i].setParent(None)
		self.graphicsViewList = []

		print("Local size")
		for idx, comboBox in enumerate(self.comboBoxList):
			
			# Recover the figure
			fig = self.figuresList[comboBox.currentIndex()]

			# Create a new plot
			self.graphicsViewList.append(FigureCanvas(fig))
			self.layoutVertList[idx].insertWidget(0, self.graphicsViewList[idx])
			

			# Get the local plot size

			width = self.graphicsViewList[idx].width()
			height = self.graphicsViewList[idx].height()
			print([width, height])

			# Resize
			self.graphicsViewList[idx].resize(totalWidth/self.resizeWidthRatio\
				[self.comboBoxPlotView.currentIndex()],totalHeight/self.resizeHeightRatio\
				[self.comboBoxPlotView.currentIndex()])

			width = self.graphicsViewList[idx].width()
			height = self.graphicsViewList[idx].height()
			print([width, height])


			self.graphicsViewList[idx].draw()

		
		print("\n")

	def createPlot(self, dim):

		fig = plt.figure()

	#	 LOAD DATA

	def changeOutput(self):
		#Get the path of the desired directory
		root = tk.Tk()
		root.withdraw()
		directoryName = filedialog.askdirectory()	

		if not directoryName:
			pass
		else:
			self.directoryName = directoryName
			self.setupData()
			self.updatePlots()
			

	def loadData(self):

		# Read data
		file = open(self.directoryName + '/data/results_misc.out', 'r')
		lines = file.readlines()
		file.close()

		# Pasing the txt file to get the results
		results = {}
		for i, line in enumerate(lines):
			key = []
			value = []
			inValue = False
			for c in line:
				if c == '=':
					inValue = True
				elif c ==' ':
					pass
				elif c == '\n':
					inValue = False
				else:
					if inValue:
						value.append(c)
					else:
						key.append(c)
			Key = "".join(key)
			Value = "".join(value)
			results[Key] = float(Value)

		# Set the Q value inside the lineEdit
		self.lineEditCapacity.setText(str(results['Q']))

		# Edit the pushButton
		self.pushButton.setText(os.path.basename(self.directoryName[:-1]))



if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()

	config = {}
	results = {}
	config['filename'] = './results/2016-12-19-07-46-21/'
	results['Q'] = 10
 
	resultsDialog = ResultsDialog(dialog, config)

 	
 	# Fire results dialog
	dialog.show()
	sys.exit(app.exec_())


