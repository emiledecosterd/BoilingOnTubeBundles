##	@package pipePlotter
#	Part of the BoilingOnTubeBundles project
#
#	Contain LongPipePlotter class and TransvPipePlotter class for plotter scheme on the GUI

# Package for the plotter
import numpy as np
import math

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from error import Error

##	PipePlotter
#	General class used to plot on the GUI GraphicsView
class PipePlotter(QtCore.QObject):

	##	__init__()
	#	Constructor of the generic plotter
	#	@param graphicsView The reference on the QGraphicsView from the GUI
	def __init__(self, graphicsView):
		# The view in which to draw
		self.view = graphicsView

		# The scene containing all the drawing
		sceneRect = QtCore.QRectF(self.view.geometry()) 
		self.scene = QtWidgets.QGraphicsScene(sceneRect)

		# Appearance of different lines
		self.outerRectPen = QtGui.QPen(QtCore.Qt.DashLine)
		self.pipeLinePen = QtGui.QPen(QtCore.Qt.SolidLine)
		self.pipeFillingBrush = QtGui.QBrush(QtCore.Qt.Dense7Pattern)
		self.cellPen = QtGui.QPen(QtCore.Qt.DotLine)
		self.fillPen = QtGui.QPen(QtCore.Qt.NoPen)
		self.axisLine = QtGui.QPen(QtCore.Qt.DashDotLine)

		# The colors
		self.hotColor = QtGui.QColor(QtCore.Qt.red)
		self.coldColor = QtGui.QColor(QtCore.Qt.blue)
	
	##	drawOuterRect()
	#	Draw the basis rectangle on the graphics view
	#	@param None
	def drawOuterRect(self):
		# Setup geometry
		baseRect = QtCore.QRectF(self.view.geometry())
		self.scene.setSceneRect(baseRect)
		origin = QtCore.QPointF(baseRect.x()+20, baseRect.y()+20)
		size = QtCore.QSizeF(baseRect.width()-40, baseRect.height()-40)
		outerRect = QtCore.QRectF(origin, size)
		self.bounds = outerRect

		# Save Bound constants whith the margins
		margin = 0.85
		self.viewTop = outerRect.y()+ outerRect.height()*(1-margin)/2
		self.viewBottom = self.viewTop + outerRect.height()*margin
		self.viewLeft = outerRect.x() + outerRect.width()*(1-margin)/2
		self.viewRight = self.viewLeft + outerRect.width()*margin
		self.viewHeight = outerRect.height()*margin
		self.viewWidth = outerRect.width()*margin

		# Draw the rectangle (inner)
		innerRect = QtCore.QRectF(QtCore.QPointF(self.viewLeft,self.viewTop ), QtCore.QSizeF(self.viewWidth, self.viewHeight))

		# Draw the rectangle
		self.scene.addRect(outerRect, self.outerRectPen)
		self.view.setScene(self.scene)

	##	updateView()
	#	Taking the view reference and update the scene dimensions,
	#	clear the scene and redraw the outer rectangle
	#	@param None
	def updateView(self):
		# The scene containing all the drawing
		sceneRect = QtCore.QRectF(self.view.geometry())
		self.scene = QtWidgets.QGraphicsScene(sceneRect)

		# Clear the scene
		self.scene.clear()

		# ReDraw rectangle
		self.drawOuterRect()

	##	addPoint()
	#	Add a point at the given position
	#	@param point QPointF
	def addPoint(self, point):
		radius = 1.5
		self.scene.addEllipse(point.x()-radius, point.y()-radius, 2.0*radius, 2.0*radius,\
			self.pipeLinePen)

##	LongPipePlotter
#	Subclass of PipePlotter for the longitudinal view scheme
class LongPipePlotter(PipePlotter):

	cells = None

	def __init__(self, view):
		super(LongPipePlotter, self).__init__(view)
		

	##	drawScheme()
	#	Draw the longitudinal scheme on the graphics view 
	#	@param geom The geometrical inputs taken from the GUI
	#	@param results Thermodynamics fields value send when the calculation is finished. Equal to 
	#	None otherwise.
	def drawScheme(self, geom, result):
		# Save the geom inputs
		self.geom = geom

		# Update and clear the view
		self.updateView()

		# Draw the pipes
		self.drawPipes(geom['Nt'])

		# Draw the cells and save the coordinates
		self.coordinates = self.drawCells(geom['Nt'], geom['n'])

		# Fill the cells
		if result is not None:
			try:
				self.fillCells(self.coordinates, result)
			except Exception as e:
				raise Error('LongPipePlotter.fillCells', e)

	##	drawCells()
	#	Draw the cells discretized and save the coordinates
	#	@param vert Number of cells to draw vertically
	#	@param hor Number of cells to draw horizontally
	def drawCells(self, vert, hor):
		# Initialization of return variables
		coordinates_x = [self.bounds.x()]
		coordinates_y = [self.bounds.y()]

		# Constants
		dx = self.bounds.width()/hor
		dy = self.bounds.height()/vert
		top = self.bounds.y()
		bottom = top + self.bounds.height()
		left = self.bounds.x()
		right = left + self.bounds.width()

		# We only draw the lines inside the outer rectangle
		vert = vert-1
		hor = hor-1

		# Draw vertical lines
		for i in range(hor):
			x = self.bounds.x() + (i+1)*dx
			coordinates_x.append(x)
			start = QtCore.QPointF(x, top)
			end = QtCore.QPointF(x, bottom)
			line = QtCore.QLineF(start, end)
			self.scene.addLine(line, self.cellPen)

		# Draw horizontal ines
		for j in range(vert):
			y = self.bounds.y() + (j+1)*dy
			coordinates_y.insert(0,y)
			start = QtCore.QPointF(left, y)
			end = QtCore.QPointF(right, y)
			line = QtCore.QLineF(start, end)
			self.scene.addLine(line, self.cellPen)

		coordinates_x.append(self.bounds.x()+self.bounds.width())
		coordinates_y.insert(0, self.bounds.y()+self.bounds.height())

		return (coordinates_x, coordinates_y)


	##	drawPipes()
	#	Draw all the pipes inside the GraphicsView
	#	@param amount Nombre of tubes rows
	def drawPipes(self, amount):

		pipeHeight = self.bounds.height()/amount/3
		distance = self.bounds.height()/amount
		centerLine = self.bounds.y() - distance/2
		
		for i in range(amount):
			centerLine = centerLine + distance
			self.drawPipe(centerLine, pipeHeight)

	##	drawPipe()
	#	Draws a single pipe within the bounds of the outer rectangle
	#	The inside of the pipe is darker than the outside so we can distinguish it better
	#	@param centerline The revolution axis Y position of the pipe
	#	@param height The height of the pipe
	def drawPipe(self, centerLine, height):

		# Setup geometry
		half = height/2
		top = centerLine-half 
		bottom = centerLine+half
		start = self.bounds.x()
		end = self.bounds.x()+self.bounds.width()

		# Draw the lines
		topStart = QtCore.QPointF(start, top)
		topEnd = QtCore.QPointF(end, top)
		topLine = QtCore.QLineF(topStart, topEnd)
		bottomStart = QtCore.QPointF(start, bottom)
		bottomEnd = QtCore.QPointF(end, bottom)
		bottomLine = QtCore.QLineF(bottomStart, bottomEnd)
		self.scene.addLine(topLine, self.pipeLinePen)
		self.scene.addLine(bottomLine, self.pipeLinePen)

		# Fill the pipes
		brushRect = QtCore.QRectF(topStart, bottomEnd)
		self.scene.addRect(brushRect, QtGui.QPen(QtCore.Qt.NoPen), self.pipeFillingBrush)


	##	fillCells()
	#	Fills the cells according to the thermodynamics varaible
	#	results. 
	#	@param coordinates The coordinates of the pipes on the plot
	#	@param field The thermodynamical field chosen by the user in the GUI
	def fillCells(self, coordinates, field):

		coordinates_x = coordinates[0]
		coordinates_y = coordinates[1]

		# Find min and max and define color range
		maxVal = field.max()
		# Bidouillage
		minVal = abs(field[1:,1:].min())


		# Draw each cell
		for i in range(1,field.shape[1]):
			for j in range(1,field.shape[0]):
									
				# Get rectangle coordinates
				top = QtCore.QPointF(coordinates_x[i-1], coordinates_y[j])
				bottom = QtCore.QPointF(coordinates_x[i], coordinates_y[j-1])
				rect = QtCore.QRectF(top, bottom)

				# Get right color
				''' /!\ To be corrected !!! '''
				val = (field[j,i]-minVal)/(maxVal-minVal)
				r = int(self.coldColor.red() + val*(self.hotColor.red()-self.coldColor.red()))
				g = 0
				b = int(self.coldColor.blue() + val*(self.hotColor.blue() - self.coldColor.blue()))
				color = QtGui.QColor(r,g,b, 200)
				brush = QtGui.QBrush(color, QtCore.Qt.Dense2Pattern)

				# Draw the rectangle
				cell = self.scene.addRect(rect, self.fillPen, brush)

##	TransvPipePlotter
#	Subclass of PipePlotter for the transversal view scheme
class TransvPipePlotter(PipePlotter):

	def __init__(self, view):
		super(TransvPipePlotter, self).__init__(view)


	##	drawScheme()
	#	Draw the transversal scheme on the graphics view 
	#	@param geom The geometrical inputs taken from the GUI
	def drawScheme(self, geom):
		self.geom = geom

		# Update graph
		self.updateView()

		# Setup ratio
		self.heightMax = self.geom['Ds']
		self.widthMax =  self.geom['Ds']

		if self.viewHeight/self.heightMax < self.viewWidth/self.widthMax :
			self.ratio = self.viewHeight/self.heightMax
		else:
			self.ratio = self.viewWidth/self.widthMax

		#Change all inputs according to ratio
		self.shellDiam = self.geom['Ds']*self.ratio
		self.pipeDiam = self.geom['D']*self.ratio
		self.verPitch = self.geom['s']*self.ratio
		self.horPitch = self.geom['sh']*self.ratio
		self.Ncol = self.geom['Nt_col']
		self.Nrow = self.geom['Nt']

		# Draw shell
		self.drawShellCircle()

		# Draw the pipes depending on the layout
		if self.geom['layout'] == 'Inline' :
			self.drawPipesInline()
		else:
			self.drawPipesStaggered()

		# Draw axis
		self.drawAxis()

	## 	drawShellCircle()
	#	Draw the Shell on the QGraphicsView 
	#	@param None
	def drawShellCircle(self):
		xHalfView = self.viewLeft + self.viewWidth/2
		yHalfView = self.viewTop + self.viewHeight/2

		origin = QtCore.QPointF(xHalfView-self.shellDiam/2, yHalfView-self.shellDiam/2)
		size = QtCore.QSizeF(self.shellDiam, self.shellDiam)
		shellCircle = QtCore.QRectF(origin, size)

		self.scene.addEllipse(shellCircle, self.pipeLinePen)

	## 	drawAPipe()
	#	Draw a pipe on the transversal view
	#	@param position QPointF, Center of the desired pipe position
	def drawAPipe(self, position):
		self.scene.addEllipse(position.x()-self.pipeDiam/2, position.y()-self.pipeDiam/2, \
			self.pipeDiam, self.pipeDiam,	self.pipeLinePen, self.pipeFillingBrush)

	## 	drawPipesInline()
	#	Draw all the pipes for Inline layout
	#	@param None
	def drawPipesInline(self):
		# Start point
		xHalfView = self.viewLeft + self.viewWidth/2
		yHalfView = self.viewTop + self.viewHeight/2

		if self.Ncol % 2 != 0:
			xStart = xHalfView-(self.Ncol-1)/2*self.horPitch
		else:
			xStart = xHalfView-(self.Ncol/2)*self.horPitch+self.horPitch/2
		if self.Nrow % 2 != 0:
			yStart = yHalfView-(self.Nrow-1)/2*self.verPitch
		else:
			yStart = yHalfView-(self.Nrow/2)*self.verPitch+self.verPitch/2
		
		xPoint = xStart
		yPoint = yStart

		for i in range(self.Ncol):
			xPoint = xStart + self.horPitch*i
			for j in range(self.Nrow):
				yPoint = yStart + self.verPitch*j
				point = QtCore.QPointF(xPoint, yPoint)
				self.drawAPipe(point)
			yPoint = yStart 

	## 	drawPipesInline()
	#	Draw all the pipes for Staggered layout
	#	@param None
	def drawPipesStaggered(self):
		# Start point
		xHalfView = self.viewLeft + self.viewWidth/2
		yHalfView = self.viewTop + self.viewHeight/2

		if self.Ncol % 2 != 0:
			xStart = xHalfView-(self.Ncol-1)/2*self.horPitch
		else:
			xStart = xHalfView-(self.Ncol/2)*self.horPitch+self.horPitch/2
		if self.Nrow % 2 != 0:
			yStart = yHalfView-(self.Nrow-1)/2*self.verPitch
		else:
			yStart = yHalfView-(self.Nrow/2)*self.verPitch+self.verPitch/2
		
		xPoint = xStart
		yPoint = yStart
		left = True

		a = self.horPitch/self.pipeDiam
		b = self.verPitch/self.pipeDiam

		#Horizontal staggered detection :
		if (b >= 0.5*math.sqrt(2*a+1)):
			for j in range(self.Nrow):
				yPoint = yStart + self.verPitch*j
				for i in range(self.Ncol):
					xPoint = xStart + self.horPitch*i
					point = QtCore.QPointF(xPoint, yPoint)
					self.drawAPipe(point)
				if left:
					xStart += self.horPitch/2
					left = False
				else:
					xStart -= self.horPitch/2
					left = True
		else :
			for i in range(self.Ncol):
					xPoint = xStart + self.horPitch*i
					for j in range(self.Nrow):
						yPoint = yStart + self.verPitch*j
						point = QtCore.QPointF(xPoint, yPoint)
						self.drawAPipe(point)
					if left:
						yStart += self.verPitch/2
						left = False
					else:
						yStart -= self.verPitch/2
						left = True

	
	## 	drawAxis()
	#	Draw the axis
	#	@param None
	def drawAxis(self):
		xHalfView = self.viewLeft + self.viewWidth/2
		yHalfView = self.viewTop + self.viewHeight/2

		# y-axis
		startLine = QtCore.QPointF(xHalfView, self.viewTop)
		endLine = QtCore.QPointF(xHalfView, self.viewBottom)
		line = QtCore.QLineF(startLine, endLine)
		self.scene.addLine(line, self.axisLine)

		# x-axis
		startLine = QtCore.QPointF(xHalfView-self.shellDiam/2, yHalfView)
		endLine = QtCore.QPointF(xHalfView+self.shellDiam/2, yHalfView)
		line = QtCore.QLineF(startLine, endLine)
		self.scene.addLine(line, self.axisLine)

