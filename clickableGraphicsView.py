##	@package	clickableGraphicsView
#
#	Contains a custom subclass to detect mouse presses.

from PyQt5 import QtWidgets, QtCore


##	QClickabeGraphicsView
#
#	Emit a the 'clicked' signal when it detects a press inside itself.
class QClickableGraphicsView(QtWidgets.QGraphicsView):

	clicked = QtCore.pyqtSignal() 

	def __init__(self, parent=None):
		super(QClickableGraphicsView, self).__init__(parent)

	def mousePressEvent(self, event):
		print('Clicked')
		self.clicked.emit()