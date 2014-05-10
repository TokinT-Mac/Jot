import sys
from PyQt4 import QtGui, QtCore


class Jot(QtGui.QTabWidget):
	def __init__(self):
		super(Jot, self).__init__()
		self.windowControls = WindowControls(self)
		self.defaultSize = (1000,600,1000,600)
		self.initUI()
		
	def initUI(self):
		self.setGeometry(*self.defaultSize)
		self.move(QtGui.QDesktopWidget().availableGeometry().center()-self.rect().center())
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setTabShape(QtGui.QTabWidget.Triangular)
		self.setStyleSheet("QTabBar::tab { height: 24px; width: 100px; }")
		self.setStyleSheet("QTabBar { border: none; padding: 0px; }")
		self.setUsesScrollButtons(False)
		self.setMovable(True)
		self.setTabsClosable(True)
		self.maximized = False
		
		
		self.TestTabs()
		self.initControls()
		self.initActions()
		
		self.setCornerWidget(self.windowControls)
		self.tabCloseRequested.connect(self.closeTab)
		self.show()
	
	def initControls(self):
		self.windowControls.closeWindow.triggered.connect(self.close)
		self.windowControls.maximizeWindow.triggered.connect(self.maximizeEvent)
		
	def initActions(self):
		newAction = QtGui.QAction('New', self)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('Create new file')
		newAction.triggered.connect(self.newFile)
		self.newAction = newAction
		
	def closeTab(self, index):
		if self.count() > 1:
			self.removeTab(index)
			self.setTabWidth()
		else:
			self.close()
		
		
	def TestTabs(self):
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		self.addTab(QtGui.QTextEdit(), 'test')
		
	def setTabWidth(self):
		default = 100
		width = self.width()-self.windowControls.width()
		perTab = width/self.count()
		if perTab < 100:
			tabWidth = perTab
			
		else:
			tabWidth = default
			
		self.setStyleSheet("QTabBar::tab { height: 24px; width: %spx; }"%str(tabWidth))
		
	def addTab(self, *args):
		super(Jot, self).addTab(*args)
		self.setTabWidth()
		
	def newFile(self):
		print 't'
		
	def maximizeEvent(self):
		if not self.maximized:
			self.lastPosition = self.mapToGlobal(self.pos())
			screen = QtGui.QDesktopWidget().availableGeometry()
			self.move(0,0)
			self.resize(screen.width(), screen.height())
			self.maximized = True
			
		else:
			self.resize(self.defaultSize[0], self.defaultSize[1])
			self.move(self.lastPosition)
			self.maximized = False
			
	def paintEvent(self, event):
		super(Jot, self).paintEvent(event)
		if self.maximized:
			backgroundColor = QtGui.QColor(QtCore.Qt.black)
			backgroundColor.setAlpha(200)
			paint = QtGui.QPainter(self)
			paint.fillRect(self.rect(), backgroundColor)
		
		
class WindowControls(QtGui.QWidget):
	def __init__(self, parent):
		super(WindowControls, self).__init__(parent)
		self.initUI()
		self.initClose()
		self.initMax()
		self.initMin()
		
	def initUI(self):
		self.closeButton = ControlButton(self)
		self.closeButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.closeButton.setIconSize(QtCore.QSize(16,16))
		self.closeButton.setAutoRaise(True)

		self.maxButton = ControlButton(self)
		self.maxButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.maxButton.setIconSize(QtCore.QSize(16,16))
		self.maxButton.setAutoRaise(True)

		self.minButton = ControlButton(self)
		self.minButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.minButton.setIconSize(QtCore.QSize(16,16))
		self.minButton.setAutoRaise(True)
			
		
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

		
def main():
	app = QtGui.QApplication(sys.argv)
	jot = Jot()
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()