##	@package	resizableDialog
#
#	Contains a custom subclass to detect mouse presses.

from PyQt5 import QtWidgets, QtCore


##	QClickabeGraphicsView
#
#	Emit a the 'clicked' signal when it detects a press inside itself.
class QResizableDialog(QtWidgets.QDialog):
	# See if we need a timer in order to reduce latency (little freezes)

	resized = QtCore.pyqtSignal() 

	def __init__(self, parent=None):
		super(QResizableDialog, self).__init__(parent)

	def resizeEvent(self, event):
			self.resized.emit()