import sys
from PyQt4 import QtGui, QtCore
import tabs
from document import Document

class Jot(QtGui.QTabWidget):
	def __init__(self):
		super(Jot, self).__init__()
		self.windowControls = WindowControls(self)
		self.documents = {}
		self.defaultSize = (1000,600,1000,600)
		self.fancyTabBar = tabs.FancyTabBar(parent=self)
		self.setTabBar(self.fancyTabBar)
		self.initUI()
		
		
	def initUI(self):
		self.setGeometry(*self.defaultSize)
		self.move(QtGui.QDesktopWidget().availableGeometry().center()-self.rect().center())
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setTabShape(QtGui.QTabWidget.Triangular)
		#self.setStyleSheet("QTabBar::tab { min-width: 8ex; padding: 50px;} QTabBar::tab:selected { margin-left: -25px; margin-right: -25px;} QTabBar::tab:!selected { margin-top: 2px;}")
		self.setStyleSheet("QTabBar { border: 10px; padding: 5px; }")
		self.setStyleSheet("QTabWidget::pane {border-top: 5px solid #C2C7CB;}")
		
		self.setUsesScrollButtons(False)
		self.setMovable(True)
		self.setTabsClosable(True)
		self.maximized = False
		self.minimized = False
		self.show()
		
		self.TestTabs()
		self.initControls()
		self.initActions()
		
		self.setCornerWidget(self.windowControls)
		self.tabCloseRequested.connect(self.closeTab)
		
	
	def initControls(self):
		self.windowControls.closeWindow.triggered.connect(self.close)
		self.windowControls.maximizeWindow.triggered.connect(self.maximizeEvent)
		self.windowControls.minimizeWindow.triggered.connect(self.minimizeEvent)
		
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
		self.newFile()
		
	def setTabWidth(self):
		default = 100
		width = self.width()-self.windowControls.width()
		perTab = width/self.count()
		if perTab < 100:
			tabWidth = perTab
			
		else:
			tabWidth = default
			
		self.setStyleSheet("QTabBar::tab { height: 24px; width: %spx; }"%str(tabWidth))
		self.update()
		
	def addTab(self, *args):
		index = super(Jot, self).addTab(*args)
		tabbar = self.tabBar()
		tabbar.setTabButton(index, QtGui.QTabBar.RightSide, tabs.TabButton())
		self.setTabWidth()
		self.setCurrentIndex(index)
		
	def newFile(self):
		doc = Document(parent = self)
		self.documents[doc.codeEditor] = doc
		self.addTab(doc.codeEditor, doc.basename)
		
	def loadFile(self):
		doc = Document(parent = self).Open()
		self.documents[doc.codeEditor] = doc
		self.addTab(doc.codeEditor, doc.basename)
			
		
	def maximizeEvent(self):
		if not self.maximized:
			self.maximized = True
			self.showMaximized()
			
		else:
			self.maximized = False
			self.showNormal()
			
	def minimizeEvent(self):
		if not self.minimized:
			self.miniized = True
			self.showMinimized()
		else:
			self.showNormal()
		
		
	def paintEvent(self, event):
		super(Jot, self).paintEvent(event)
		if self.maximized:
			backgroundColor = QtGui.QColor(QtCore.Qt.black)
			backgroundColor.setAlpha(200)
			paint = QtGui.QPainter(self)
			paint.fillRect(self.rect(), backgroundColor)
			paint.end()
				
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
			
'''class Document(QtGui.QWidget):
	def __init__(self, parent = None, mode = 'new',):
		
		QtGui.QWidget.__init__(self, parent)
			
		self.codeEditor = editor.CodeEditor()
		self.formatter = Highlighter(self.codeEditor.document(), 'python')
		
		self.shortcutSave = QtGui.QShortcut('CTRL+S', self.codeEditor)
		self.connect(self.shortcutSave, QtCore.SIGNAL("activated()"), self.saveFile)
		
		self.shortcutOpen = QtGui.QShortcut('CTRL+O', self.codeEditor)
		self.connect(self.shortcutOpen, QtCore.SIGNAL('activated()'), self.parent().loadFile)
		
		self.shortcutNew = QtGui.QShortcut('CTRL+N', self.codeEditor)
		self.connect(self.shortcutNew, QtCore.SIGNAL('activated()'), self.parent().newFile)
		
		if mode == 'load':
			self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
			self.basename = os.path.basename(str(self.filename))
			self.loadFile()
		if mode == 'new':
			self.filename = None
			self.basename = 'new'
			
	def loadFile(self):
		with open(self.filename, 'r') as file:
			text = file.read()
			print 'loaded'
			self.codeEditor.setPlainText(text)
			
	def saveFile(self):
		if not self.filename:
			self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
		
		with open(self.filename, 'w') as file:
			file.write(self.CodeEditor.document().toPlainText())
			

		'''
def main():
	app = QtGui.QApplication(sys.argv)
	jot = Jot()
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()