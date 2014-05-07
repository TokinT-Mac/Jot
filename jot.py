import sys
from PyQt4 import QtGui, QtCore


class Jot(QtGui.QTabWidget):
	def __init__(self):
		super(Jot, self).__init__()
		self.windowControls = WindowControls(self)
		self.initUI()
		
	def initUI(self):
		self.setGeometry(500,300,500,300)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setTabShape(QtGui.QTabWidget.Triangular)
		self.setStyleSheet("QTabBar::tab { height: 24px; width: 100px; }")
		self.setUsesScrollButtons(False)
		self.setMovable(True)
		self.setTabsClosable(True)
		
		
		self.TestTabs()
		self.initControls()
		self.initActions()
		
		self.setCornerWidget(self.windowControls)
		self.tabCloseRequested.connect(self.closeTab)
		self.show()
	
	def initControls(self):
		self.windowControls.closeWindow.triggered.connect(self.close)
		
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
		
	
		
class WindowControls(QtGui.QWidget):
	def __init__(self, parent):
		super(WindowControls, self).__init__(parent)
		self.initUI()
		self.initClose()
		self.initMax()
		self.initMin()
		
	def initUI(self):
		self.closeButton = QtGui.QToolButton(self)
		self.closeButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.closeButton.setIconSize(QtCore.QSize(16,16))
		self.closeButton.setAutoRaise(True)

		self.maxButton = QtGui.QToolButton(self)
		self.maxButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.maxButton.setIconSize(QtCore.QSize(16,16))
		self.maxButton.setAutoRaise(True)

		self.minButton = QtGui.QToolButton(self)
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
		
	def connectClose(self, Action):
		self.closeButton.setDefaultAction(Action)

		
def main():
	app = QtGui.QApplication(sys.argv)
	jot = Jot()
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()