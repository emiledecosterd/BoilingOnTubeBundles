import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import math


class PipeDrawing(object):
	'''
	This class manages all the drawings of the pipe 
	and the rendition of the simulation resutls
	'''
	cells = None

	def __init__(self, graphicsView):

		# The view in which to draw
		self.view = graphicsView

		# The scene containing all the drawing
		sceneRect = QRectF(self.view.geometry()) 
		self.scene = QGraphicsScene(sceneRect)

		# Appearance of different lines
		self.outerRectPen = QPen(Qt.DashLine)
		self.pipeLinePen = QPen(Qt.SolidLine)
		self.pipeFillingBrush = QBrush(Qt.Dense7Pattern)
		self.cellPen = QPen(Qt.DotLine)
		self.fillPen = QPen(Qt.NoPen)

	def updateView(self):
		# The scene containing all the drawing
		sceneRect = QRectF(self.view.geometry())
		self.scene = QGraphicsScene(sceneRect)

		# Clear the scene
		self.scene.clear()

		# ReDraw rectangle
		self.drawOuterRect()

	def drawOuterRect(self):
		''' 
		Draws the outer rectangle, which will be the boundary of our system 
		/!\ Call this method before all other drawing methods, at best in init /!\
		'''
		# Setup geometry
		baseRect = QRectF(self.view.geometry())
		self.scene.setSceneRect(baseRect)
		origin = QPointF(baseRect.x()+20, baseRect.y()+20)
		size = QSizeF(baseRect.width()-40, baseRect.height()-40)
		outerRect = QRectF(origin, size)
		self.bounds = outerRect # Keep a trace of the rectangle in which we will draw the pipes

		# Draw the rectangle
		self.scene.addRect(outerRect, self.outerRectPen)
		self.view.setScene(self.scene)


	def drawCells(self, vert, hor):
		'''
		Draws the discretization cells in the rectangle
		Inputs:
			-> vert: number of cells to draw vertically
			-> hor: number of cells to draw horizontally
		'''

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
			start = QPointF(x, top)
			end = QPointF(x, bottom)
			line = QLineF(start, end)
			self.scene.addLine(line, self.cellPen)

		# Draw horizontal ines
		for j in range(vert):
			y = self.bounds.y() + (j+1)*dy
			coordinates_y.insert(0,y)
			start = QPointF(left, y)
			end = QPointF(right, y)
			line = QLineF(start, end)
			self.scene.addLine(line, self.cellPen)

		coordinates_x.append(self.bounds.x()+self.bounds.width())
		coordinates_y.insert(0, self.bounds.y()+self.bounds.height())

		return (coordinates_x, coordinates_y)


	def drawPipes(self, amount):

		pipeHeight = self.bounds.height()/amount/3
		distance = self.bounds.height()/amount
		centerLine = self.bounds.y() - distance/2
		
		for i in range(amount):
			centerLine = centerLine + distance
			self.drawPipe(centerLine, pipeHeight)


	def drawPipe(self, centerLine, height):
		'''
		Draws a single pipe within the bounds of the outer rectangle
		The inside of the pipe is darker than the outside so we can distinguish it better

		Inputs:
			-> centerLine: the revolution axis y position of the pipe 
			-> height: the height of the pipe
		'''
		# Setup geometry
		half = height/2
		top = centerLine-half 
		bottom = centerLine+half
		start = self.bounds.x()
		end = self.bounds.x()+self.bounds.width()

		# Draw the lines
		topStart = QPointF(start, top)
		topEnd = QPointF(end, top)
		topLine = QLineF(topStart, topEnd)
		bottomStart = QPointF(start, bottom)
		bottomEnd = QPointF(end, bottom)
		bottomLine = QLineF(bottomStart, bottomEnd)
		self.scene.addLine(topLine, self.pipeLinePen)
		self.scene.addLine(bottomLine, self.pipeLinePen)

		# Fill the pipes
		brushRect = QRectF(topStart, bottomEnd)
		self.scene.addRect(brushRect, QPen(Qt.NoPen), self.pipeFillingBrush)


	def fillCells(self, coordinates, field):

		if self.cells is not None:
			for i in range(1, len(self.cells)):
				self.scene.removeItem(self.cells[i])
			del self.cells[:]
		else:
			self.cells = []

		coordinates_x = coordinates[0]
		coordinates_y = coordinates[1]

		#print(coordinates_x)
		#print(coordinates_y)

		# Find min and max and define color range
		maxVal = field.max()
		# Bidouillage
		minVal = abs(field[1:,1:].min())


		# Draw each cell
		for i in range(1,field.shape[1]):
			for j in range(1,field.shape[0]):

				#print('(i,j) = (%i,%i)' %(i,j))
									
				# Get rectangle coordinates
				top = QPointF(coordinates_x[i-1], coordinates_y[j])
				bottom = QPointF(coordinates_x[i], coordinates_y[j-1])
				rect = QRectF(top, bottom)

				#print(field[j,i])

				# Get right color
				''' /!\ To be corrected !!! '''
				val = (field[j,i]-minVal)/(maxVal-minVal)/5 + 0.7
				color = QColor()
				color.setHsvF(val, 0.5,0.5,0.5)
				brush = QBrush(color, Qt.Dense2Pattern)

				# Draw the rectangle
				cell = self.scene.addRect(rect, self.fillPen, brush)
				self.cells.append(cell)


class CutDrawing(object):
	'''
	This class manages all the drawings of the cut graph
	'''

	def __init__(self, graphicsView):

		# The view in which to draw
		self.view = graphicsView

		# The scene containing all the drawing
		sceneRect = QRectF(self.view.geometry()) 
		self.scene = QGraphicsScene(sceneRect)

		# Appearance of different lines
		self.outerRectPen = QPen(Qt.DashLine)
		self.pipeLinePen = QPen(Qt.SolidLine)
		self.axisLine = QPen(Qt.DashDotLine)
		self.pipeFillingBrush = QBrush(Qt.Dense7Pattern)

	def updateView(self):
		# The scene containing all the drawing
		sceneRect = QRectF(self.view.geometry())
		self.scene = QGraphicsScene(sceneRect)

		# Clear the scene
		self.scene.clear()

		# ReDraw rectangle
		self.drawOuterRect()

	def drawOuterRect(self):
		''' 
		Draws the outer rectangle, which will be the boundary of our system 
		/!\ Call this method before all other drawing methods, at best in init /!\
		'''
		# Setup geometry
		baseRect = QRectF(self.view.geometry())
		self.scene.setSceneRect(baseRect)
		origin = QPointF(baseRect.x()+20, baseRect.y()+20)
		size = QSizeF(baseRect.width()-40, baseRect.height()-40)
		outerRect = QRectF(origin, size)

		# Save Bound constants whith the margins
		margin = 0.85
		self.viewTop = outerRect.y()+ outerRect.height()*(1-margin)/2
		self.viewBottom = self.viewTop + outerRect.height()*margin
		self.viewLeft = outerRect.x() + outerRect.width()*(1-margin)/2
		self.viewRight = self.viewLeft + outerRect.width()*margin
		self.viewHeight = outerRect.height()*margin
		self.viewWidth = outerRect.width()*margin

		# Draw the rectangle (inner)
		innerRect = QRectF(QPointF(self.viewLeft,self.viewTop ), QSizeF(self.viewWidth, self.viewHeight))
		self.scene.addRect(innerRect, self.outerRectPen)
		# self.addPoint(QPointF(self.viewLeft, self.viewTop))

		# Draw the rectangle
		self.scene.addRect(outerRect, self.outerRectPen)
		self.view.setScene(self.scene)

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

		# Draw the pipes
		self.drawPipesStaggered()

		# Draw axis
		self.drawAxis()


	def drawShellCircle(self):
		xHalfView = self.viewLeft + self.viewWidth/2
		yHalfView = self.viewTop + self.viewHeight/2

		origin = QPointF(xHalfView-self.shellDiam/2, yHalfView-self.shellDiam/2)
		size = QSizeF(self.shellDiam, self.shellDiam)
		shellCircle = QRectF(origin, size)

		self.scene.addEllipse(shellCircle, self.pipeLinePen)

	def drawAPipe(self, position):
		self.scene.addEllipse(position.x()-self.pipeDiam/2, position.y()-self.pipeDiam/2, \
			self.pipeDiam, self.pipeDiam,	self.pipeLinePen, self.pipeFillingBrush)

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
				point = QPointF(xPoint, yPoint)
				self.drawAPipe(point)
			yPoint = yStart 

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
					point = QPointF(xPoint, yPoint)
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
						point = QPointF(xPoint, yPoint)
						self.drawAPipe(point)
					if left:
						yStart += self.verPitch/2
						left = False
					else:
						yStart -= self.verPitch/2
						left = True

	

	def drawAxis(self):
		xHalfView = self.viewLeft + self.viewWidth/2
		yHalfView = self.viewTop + self.viewHeight/2

		# y-axis
		startLine = QPointF(xHalfView, self.viewTop)
		endLine = QPointF(xHalfView, self.viewBottom)
		line = QLineF(startLine, endLine)
		self.scene.addLine(line, self.axisLine)

		# x-axis
		startLine = QPointF(xHalfView-self.shellDiam/2, yHalfView)
		endLine = QPointF(xHalfView+self.shellDiam/2, yHalfView)
		line = QLineF(startLine, endLine)
		self.scene.addLine(line, self.axisLine)


	def addPoint(self, point):
		radius = 1.5
		self.scene.addEllipse(point.x()-radius, point.y()-radius, 2.0*radius, 2.0*radius,\
			self.pipeLinePen)
