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

	def drawOuterRect(self):
		''' 
		Draws the outer rectangle, which will be the boundary of our system 
		/!\ Call this method before all other drawing methods, at best in init /!\
		'''
		# Setup geometry
		baseRect = QRectF(self.view.geometry())
		print(baseRect)
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
				val = (field[j,i]-minVal)/(maxVal-minVal)/5
				print(val)
				color = QColor()
				color.setHsvF(val, 0.5,0.5,0.5)
				brush = QBrush(color, Qt.Dense2Pattern)

				# Draw the rectangle
				self.scene.addRect(rect, self.fillPen, brush)


