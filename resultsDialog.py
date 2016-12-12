##	@package resultsDialog
#	Results display, plots
#
#	Dialog window used to display all the plots and the heat transfered in the simulation

# Package for the results dialog

import sys, os
import tkinter as tk
from tkinter import filedialog

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from resultsDialogGUI import Ui_Dialog

from PIL import Image
from PIL.ImageQt import ImageQt


##	ResultsDialog
#	Plots and results manager
class ResultsDialog(Ui_Dialog):
	
	##	Default constructor
	#	@param dialog QtWidgets.QDialog
	def __init__(self, dialog, config):
		Ui_Dialog.__init__(self) 
		self.setupUi(dialog) 

		self.dialog = dialog

		# Global variables
		directoryName = ('./figures/' + config['initTime'])

		# Setup the view
		self.setupView(directoryName)


	#	SETUP METHODS

	def setupView(self, directoryName):
		# Setup
		self.setupLists()

		# Load images 
		self.loadImages(directoryName)
		self.loadData(directoryName)

		# Setup signals
		self.comboBoxPlotView.currentIndexChanged.connect(self.updatePlotLayout)
		self.pushButton.clicked.connect(self.changeOutput)

		# Initialize layout
		self.addNewPlot(0,0)


	def setupLists(self):

		# Setup widgets lists
		self.layoutHorList = []
		self.layoutVertList = []
		self.comboBoxList = []
		self.graphicsViewList = []
		self.imagesList = []

		# Setup Plot Label (Pretty)
		self.prettyPlotName = ['Plot Tw', 'Plot Pw', 'Plot Twf', 'Plot Pwf', 'Plot x wf', 'Plot eps']
		self.plotName = ['T_w','P_w','T_wf','P_wf','x_wf', 'eps']

		self.nPlots = [1, 4, 6]
		# Setup Plot Layout indexes

	def loadImages(self, directoryName):

		for key in self.plotName:
			imagePath = (directoryName + '/plot' + key + '.png')

			self.imagesList.append(QtGui.QPixmap(imagePath))
			print(self.imagesList[-1])
		
	#	PLOTS METHODS

	def addNewPlot(self, row, column):

		# Create new objects
		self.layoutHorList.append(QtWidgets.QHBoxLayout(self.dialog))
		spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.layoutHorList[-1].addItem(spacer)
		self.comboBoxList.append(QtWidgets.QComboBox(self.dialog))
		self.layoutHorList[-1].addWidget(self.comboBoxList[-1])
		self.layoutVertList.append(QtWidgets.QVBoxLayout())
		self.graphicsViewList.append(QResizableGraphicsView(self.dialog))
		# self.graphicsViewList.append(QtWidgets.QLabel(self.dialog))
		self.layoutVertList[-1].addWidget(self.graphicsViewList[-1])
		self.layoutVertList[-1].addLayout(self.layoutHorList[-1])
		self.gridLayout.addLayout(self.layoutVertList[-1], row, column)

		# Setup Combobox
		self.comboBoxList[-1].setMinimumSize(QtCore.QSize(190,0))
		self.comboBoxList[-1].setMaximumSize(QtCore.QSize(190,16777215))
		for item in range(len(self.prettyPlotName)) :
			self.comboBoxList[-1].addItem('')
			self.comboBoxList[-1].setItemText(item, self.prettyPlotName[item])
		self.comboBoxList[-1].currentIndexChanged.connect(self.setPlotImage)
		

	def updatePlotLayout(self, layoutIndex):
		# Clear all plots
		for i in range(len(self.graphicsViewList)):
			self.layoutHorList[i].setParent(None)
			self.layoutVertList[i].setParent(None)
			self.comboBoxList[i].setParent(None)
			self.graphicsViewList[i].setParent(None)

		# Number of plots to displays
		nPlots = self.nPlots[layoutIndex]

		# Add plot to the gridlayout
		if nPlots == 1:
			self.addNewPlot(0,0)
		for i in range(2):
			for j in range(round(nPlots/2)):
				self.addNewPlot(i,j)
				self.comboBoxList[-1].setCurrentIndex(j+(nPlots/2)*i)

	def setPlotImage(self, imageIndex):
		# Find the sender
		comboBoxSender = self.dialog.sender()

		plotIndex = self.comboBoxList.index(comboBoxSender)

		#	Create scene according to the Qgraphicsview size
		sceneRect = QtCore.QRectF(self.graphicsViewList[-1].geometry()) 
		scene = QtWidgets.QGraphicsScene(sceneRect)

		#	Set the image to plot
		pixItem =  QtWidgets.QGraphicsPixmapItem(self.imagesList[imageIndex])
		scene.addItem(pixItem)

		self.graphicsViewList[-1].fitInView(pixItem)
		self.graphicsViewList[-1].show()

		# scaledPixmap = self.imagesList[imageIndex].scaled(self.graphicsViewList[plotIndex].size(), QtCore.Qt.KeepAspectRatio)
		# self.graphicsViewList[plotIndex].setPixmap(scaledPixmap)



	#	 LOAD DATA

	def changeOutput(self):
		#Get the path of the desired directory
		root = tk.Tk()
		root.withdraw()
		directoryName = filedialog.askdirectory()

		if not directoryName:
			pass
		else:
			self.setupView(directoryName)
			

	def loadData(self, directoryName):

		# Read data
		file = open(directoryName + '/results_misc.out', 'r')
		lines = file.readlines()
		file.close()

		# Pasing the txt file to get the results
		results = {}
		for i, line in enumerate(lines):
			print(line)
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
		self.pushButton.setText(os.path.basename(directoryName))




class QResizableGraphicsView(QtWidgets.QGraphicsView):
	# See if we need a timer in order to reduce latency (little freezes)

	resized = QtCore.pyqtSignal() 

	def __init__(self, parent=None):
		super(QResizableGraphicsView, self).__init__(parent)

	def resizeEvent(self, event):
			self.resized.emit()

	


if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()

	config = {}
	results = {}
	config['initTime'] = '201612192002'
	results['Q'] = 10
 
	resultsDialog = ResultsDialog(dialog, config)
 	
 	# Fire results dialog
	dialog.show()
	sys.exit(app.exec_())


