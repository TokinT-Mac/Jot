import sys
from PyQt4 import QtGui, QtCore
import tabs
from document import Document
from tabs import FancyTabWidget
from winControl import WindowControls
import logging
moduleLogger = logging.getLogger('Jot')
LOG_LEVEL = logging.DEBUG
LOG_FILE = 'debug.log'
logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILE, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Jot(FancyTabWidget):
	def __init__(self):
		super(Jot, self).__init__()
		#self.tabWidget = FancyTabWidget(self)
		self.windowControls = WindowControls(self) #create the Max, Min, & Close buttons
		#self.tabWidget.show()
		self.documents = {}
		self.defaultSize = (1000,600,1000,600)
		#self.fancyTabBar = tabs.FancyTabBar(parent=self)
		#self.setTabBar(self.fancyTabBar)
		#self.tabButtons = SmartOrderList()
		self.initUI()
		
		
		#self.tabBar().tabMoved.connect(self.tabButtons.moveItem)
		
	def initUI(self):
		self.setGeometry(*self.defaultSize)
		self.move(QtGui.QDesktopWidget().availableGeometry().center()-self.rect().center())
		
		#hbox = QtGui.QHBoxLayout()
		#hbox.setSpacing(0)
		##hbox.setMargin(0)
		#hbox.addWidget(self.tabWidget)
		#self.setLayout(hbox)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		#self.setTabShape(QtGui.QTabWidget.Triangular)
		#self.setStyleSheet("QTabBar::tab { min-width: 8ex; padding: 50px;} QTabBar::tab:selected { margin-left: -25px; margin-right: -25px;} QTabBar::tab:!selected { margin-top: 2px;}")
		#self.setStyleSheet("QTabBar { border: 10px; padding: 5px; }")
		#self.setStyleSheet("QTabWidget::pane {border: 0px solid #C2C7CB;} QTabWidget::tab-bar { down: 5px;}")
		
		#self.setUsesScrollButtons(False)
		#self.setMovable(True)
		#self.setTabsClosable(True)
		self.maximized = False
		self.minimized = False
		self.show()
		
		self.TestTabs()
		self.initControls()
		self.initActions()
		
		self.setCornerWidget(self.windowControls)
		self.tabCloseRequested.connect(self.closeTab)
		
	
	def initControls(self):
		self.windowControls.close.connect(self.close)
		self.windowControls.maximize.connect(self.maximizeEvent)
		self.windowControls.minimize.connect(self.minimizeEvent)
		
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
		
	def closeTabById(self, id):
		print 'closing %s'%str(id)
		index = self.tabButtons.getIndexById(id)
		self.tabButtons.removeItem(index)
		self.closeTab(index)
		
	def TestTabs(self):
		self.newFile()
		
	def setTabWidth(self):
		default = 100
		width = self.width()-self.windowControls.width()
		print width
		print self.windowControls.sizeHint().width()
		perTab = width/self.count()
		if perTab < 122:
			tabWidth = perTab-22
			
		else:
			tabWidth = default
			
		self.setStyleSheet("QTabBar::tab { height: 24px; width: %spx; }"%str(int(tabWidth)))
		print tabWidth
		self.update()
		
	def addTab(self, document):
		index = super(Jot, self).addTab(document)
		print index
		
	def newFile(self):
		doc = Document(parent = self)
		#self.documents[doc.codeEditor] = doc
		self.addTab(doc)
		
	def loadFile(self):
		doc = Document(parent = self).Open()
		if not doc == False:
			#self.documents[doc.codeEditor] = doc
			self.addTab(doc)
		
			
		
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
				
class Jot2(QtGui.QWidget):
	def __init__(self):
		super(Jot2, self).__init__(self)
		
			
def main():
	app = QtGui.QApplication(sys.argv)
	jot = Jot()
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()