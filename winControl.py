from PyQt4 import QtGui, QtCore
import logging
moduleLogger = logging.getLogger('winControl')

class WindowControls(QtGui.QWidget):
	def __init__(self, parent):
		super(WindowControls, self).__init__(parent=parent)
		self.initUI()
		self.initClose()
		self.initMax()
		self.initMin()
		
		self.minimize = self.minimizeWindow.triggered
		self.maximize = self.maximizeWindow.triggered
		self.close = self.closeWindow.triggered
		self.show()
		
	def initUI(self):
		self.closeButton = ControlButton(self)
		self.maxButton = ControlButton(self)
		self.minButton = ControlButton(self)
		
		for button in [self.closeButton, self.maxButton, self.minButton]:
			button.setStyleSheet("QToolButton { border: none; padding: 0px; margin: 0px; }")
			button.setIconSize(QtCore.QSize(16,16))
			button.setAutoRaise(True)
			
		hbox = QtGui.QHBoxLayout()
		hbox.setSpacing(0)
		hbox.setMargin(0)
		hbox.addWidget(self.minButton)
		hbox.addWidget(self.maxButton)
		hbox.addWidget(self.closeButton)
		
		self.setLayout(hbox)
		
	def initClose(self):
		self.closeWindow = QtGui.QAction('Close', self)
		closeIcon = QtGui.QIcon()
		closeIcon.addFile('images/x-grey.svg', mode=QtGui.QIcon.Normal)
		closeIcon.addFile('images/x-red.svg', mode=QtGui.QIcon.Active)
		self.closeWindow.setIcon(closeIcon)
		self.closeButton.setDefaultAction(self.closeWindow)
		
	def initMax(self):
		self.maximizeWindow = QtGui.QAction('Maximize', self)
		maxIcon = QtGui.QIcon()
		maxIcon.addFile('images/maximize-blue.svg', mode=QtGui.QIcon.Active)
		maxIcon.addFile('images/circle-grey.svg', mode=QtGui.QIcon.Normal)
		self.maximizeWindow.setIcon(maxIcon)
		self.maxButton.setDefaultAction(self.maximizeWindow)
		
	def initMin(self):
		self.minimizeWindow = QtGui.QAction('Minimize', self)
		minIcon = QtGui.QIcon()
		minIcon.addFile('images/minimize-blue.svg', mode=QtGui.QIcon.Active)
		minIcon.addFile('images/circle-grey.svg', mode=QtGui.QIcon.Normal)
		self.minimizeWindow.setIcon(minIcon)
		self.minButton.setDefaultAction(self.minimizeWindow)
		
	'''def mousePressEvent(self, event):
		self.offset = event.pos()

	def mouseMoveEvent(self, event):
		x=event.globalX()
		y=event.globalY()
		x_w = self.offset.x()
		y_w = self.offset.y()
		self.parent().move(x-x_w, y-y_w)
		'''
	def move(self, *args):
		self.parent().move(*args)
		
class ControlButton(QtGui.QToolButton):
	def mousePressEvent(self, event):
		localOffset = event.pos()
		widgetOffset = self.mapToParent(localOffset)
		globalOffset = self.parent().mapToParent(widgetOffset)

		self.offset = globalOffset
		self.jitter = 0
		self.moved = False

		super(ControlButton, self).mousePressEvent(event)
		
	def mouseMoveEvent(self, event):
		if self.offset:
			self.jitter += 1
			
		if self.jitter > 5:
			x=event.globalX()
			y=event.globalY()
			x_w = self.offset.x()
			y_w = self.offset.y()
			self.parent().move(x-x_w, y-y_w)

			self.moved = True
		
	def mouseReleaseEvent(self, event):
		if self.moved:
			self.moved = False
			self.offset = None
		else:
			super(ControlButton, self).mouseReleaseEvent(event)
			
			