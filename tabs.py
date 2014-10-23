from PyQt4 import QtGui, QtCore
import uuid

class FramelessTabWidget(QtGui.QWidget):
	pass
	
class FancyTabBar(QtGui.QTabBar):
	def __init__(self, parent=None):
		super(FancyTabBar, self).__init__(parent)
		self.tabCount = 1
		self.setStyleSheet("""
		QTabBar::tab { 
			height: 24px; 
			margin-left: -8px; 
			margin-right: 0px; 
			padding-left: 15px; 
			padding-right: 15px;
				}
		QTabBar::tab:only-one {
			margin-left: 0px;
				}
		QTabBar::tab:first { 
			margin-left: 0px;
				}
		""")
		
		#self.setStyleSheet("QTabWidget::tab-bar {left: 5px;} QTabBar::tab:!selected { margin-top: 2px;} QTabBar::tab:selected {margin-left: -4px; margin-right: -4px;} QTabBar::tab:first:selected { margin-left: 0;} QTabBar::tab:last:selected { margin-right: 0;} QTabBar::tab:only-one { margin: 0;}")
		#self.setStyleSheet("QTabBar { border: none; padding: 0px; }")
			
		
class TabButton(QtGui.QToolButton):

	clicked = QtCore.pyqtSignal(str)
	
	def __init__(self, *args):
		super(TabButton, self).__init__(*args)
		self.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.setIconSize(QtCore.QSize(15,15))
		self.setAutoRaise(True)
		self.id = uuid.uuid4().hex
		print self.id
		#Load Icons
		self.iconClean = QtGui.QIcon()
		self.iconClean.addFile('images/check-green.svg', mode=QtGui.QIcon.Normal)
		self.iconClean.addFile('images/x-green.svg', mode=QtGui.QIcon.Active)
		
		self.iconDirty = QtGui.QIcon()
		self.iconDirty.addFile('images/check-red.svg', mode=QtGui.QIcon.Normal)
		self.iconDirty.addFile('images/x-red.svg', mode=QtGui.QIcon.Active)
		
		#set Icon as clean on creation
		self.setClean()
		
		#setup actions
		self.buttonAction = QtGui.QAction(self)
		self.buttonAction.triggered.connect(self.activated)
		self.setDefaultAction(self.buttonAction)
		
		clicked = QtCore.pyqtSignal(int)
		
	def __repr__(self):
		return self.id+'\n'
	def setClean(self):
		self.setIcon(self.iconClean)
		
	def setDirty(self):
		self.setIcon(self.iconDirty)
		
	def activated(self, action):
		self.clicked.emit(self.id)
		
class FancyTabWidget(QtGui.QTabWidget):
	def __init__(self, defaultTabWidth = 100, *args ):
		super(FancyTabWidget, self).__init__(*args)
		self.fancyTabBar = FancyTabBar(parent=self)
		self.setTabBar(self.fancyTabBar)
		self.tabButtons = SmartOrderList()
		self.tabBar().tabMoved.connect(self.tabButtons.moveItem)
		
		self.defaultTabWidth = defaultTabWidth
		
		
	def setOptions(self):
		self.setTabShape(QtGui.QTabWidget.Triangular)
		#self.setStyleSheet("QTabBar::tab { min-width: 8ex; padding: 50px;} QTabBar::tab:selected { margin-left: -25px; margin-right: -25px;} QTabBar::tab:!selected { margin-top: 2px;}")
		self.setStyleSheet("QTabBar { border: 10px; padding: 5px; }")
		self.setStyleSheet("QTabWidget::pane {border-top: 5px solid #C2C7CB;}")
		
		self.setUsesScrollButtons(False)
		self.setMovable(True)
		self.setTabsClosable(True)

		self.tabCloseRequested.connect(self.closeTab)
		
	def closeTab(self, index):
		if self.count() > 1:
			self.removeTab(index)


		
	def setTabWidth(self):
		tabBarWidth = self.width
		if not self.cornerWidget() == 0:
			tabBarWidth = tabBarWidth - self.cornerWidget().width()

		perTab = int(tabBarWidth/self.count())
		
		if perTab < self.defaultTabWidth + 22:
			tabWidth = perTab-22
			
		else:
			tabWidth = self.defaultTabWidth
		
		self.setStyleSheet("QTabBar::tab { height: 24px; width: %spx; }"%str(tabWidth))
		
	def addTab(self, document):
		index = super(Jot, self).addTab(document.codeEditor, document.basename)
		tabbar = self.tabBar()
		tabbar.setTabButton(index, QtGui.QTabBar.RightSide, document.StatusIcon)
		self.setTabWidth()
		self.setCurrentIndex(index)
		
	def newFile(self):
		doc = Document(parent = self)
		#self.documents[doc.codeEditor] = doc
		self.addTab(doc)
		
	def loadFile(self):
		doc = Document(parent = self).Open()
		if not doc == False:
			#self.documents[doc.codeEditor] = doc
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
			
class SmartOrderList(object):
	def __init__(self):
		self.items = []
		
		
	def addItem(self, item):
		self.items.append(item)
		
	def removeItem(self, index):
		return self.items.pop(index)
		
	def removeItemById(self, id):
		index = self.getIndexById(id)
		if index:
			self.removeItem(index)
			return index
		return None
			
			
	def moveItem(self, indexFrom, indexTo):
		print 'moving %s to %s'%(str(indexFrom), str(indexTo))
		print self.items
		item = self.items.pop(indexFrom)
		self.items.insert(indexTo, item)
		print self.items
		
	def getItemById(self, id):
		for item in self.items:
			if item.id == id:
				return item
				
		return None
	
	def getIndex(self, item):
		index = self.items.index(item)
		print index
		return index
		
	def getIndexById(self, id):
		item = self.getItemById(id)
		if item:
			return self.getIndex(item)
			
		return None
		
		
			