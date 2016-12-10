##	@package resultsDialog
#	Results display, plots
#
#	Dialog window used to display all the plots and the heat transfered in the simulation

# Package for the results dialog

import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from resultsDialogGUI import Ui_Dialog



##	ResultsDialog
#	Plots and results manager
class ResultsDialog(Ui_Dialog):
	
	##	Default constructor
	#	@param dialog QtWidgets.QDialog
	def __init__(self, dialog, results):
		Ui_Dialog.__init__(self) 
		self.setupUi(dialog) 

		# Setup
		self.setupLists()

		# Setup signals
		self.comboBoxPlotView.currentIndexChanged.connect(self.updatePlotLayout)

		# Initialize layout
		self.addNewPlot(0,0)


	def setupLists(self):

		# Setup widgets lists
		self.layoutHorList = []
		self.layoutVertList = []
		self.comboBoxList = []
		self.graphicsViewList = []

		# Setup Plot Label (Pretty)
		self.prettyPlotName = ['Plot Th', 'Plot Tc', 'Plot x']
		self.plotName = ['Th', 'Tc', 'x']

		# Setup Plot Layout indexes
		self.nPlots = [1, 4, 6]
		

	def addNewPlot(self, row, column):

		# Create new objects
		self.layoutHorList.append(QtWidgets.QHBoxLayout())
		spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.layoutHorList[-1].addItem(spacer)
		self.comboBoxList.append(QtWidgets.QComboBox())
		self.layoutHorList[-1].addWidget(self.comboBoxList[-1])
		self.layoutVertList.append(QtWidgets.QVBoxLayout())
		self.graphicsViewList.append(QResizableGraphicsView())
		self.layoutVertList[-1].addWidget(self.graphicsViewList[-1])
		self.layoutVertList[-1].addLayout(self.layoutHorList[-1])
		self.gridLayout.addLayout(self.layoutVertList[-1], row, column)

		# Setup Combobox
		self.comboBoxList[-1].setMinimumSize(QtCore.QSize(190,0))
		self.comboBoxList[-1].setMaximumSize(QtCore.QSize(190,16777215))
		for item in range(len(self.prettyPlotName)) :
			self.comboBoxList[-1].addItem('')
			self.comboBoxList[-1].setItemText(item, self.prettyPlotName[item])
		

	def updatePlotLayout(self, index):
		# Clear all plots
		for i in range(len(self.graphicsViewList)):
			self.layoutHorList[i].setParent(None)
			self.layoutVertList[i].setParent(None)
			self.comboBoxList[i].setParent(None)
			self.graphicsViewList[i].setParent(None)

		# Number of plots to displays
		nPlots = self.nPlots[index]

		# Add plot to the gridlayout
		if nPlots == 1:
			self.addNewPlot(0,0)
		for i in range(2):
			for j in range(round(nPlots/2)):
				self.addNewPlot(i,j)
				self.comboBoxList[-1].setCurrentIndex(j+(nPlots/2)*i)

	def fillGUI(self,)



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
 
	resultsDialog = ResultsDialog(dialog)
 	
 	# Fire results dialog
	dialog.show()
	sys.exit(app.exec_())


