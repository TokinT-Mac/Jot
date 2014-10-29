from PyQt4 import QtGui, QtCore
import uuid
import logging
moduleLogger = logging.getLogger('tabModule') 

class FramelessTabWidget(QtGui.QWidget):
	pass
	
class FancyTabBar(QtGui.QTabBar):

	tabCloseRequested = QtCore.pyqtSignal(tuple) #add signal for new id based tabButtons emits (tabButton.id, tabBar-index)
	
	def __init__(self, parent=None):
		super(FancyTabBar, self).__init__(parent)
		self.tabIndex = TabIndex() #create tabIndex - maps tabButton and id to physical position in tabbar. tabs represented as (tabButton.id, tabButton)
		super(FancyTabBar, self).tabMoved.connect(self.tabIndex.moveTab) #connect tab move signal to tabIndex
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
		self.log = moduleLogger.getChild('FancyTabBar') #setup logging
		
		#self.setStyleSheet("QTabWidget::tab-bar {left: 5px;} QTabBar::tab:!selected { margin-top: 2px;} QTabBar::tab:selected {margin-left: -4px; margin-right: -4px;} QTabBar::tab:first:selected { margin-left: 0;} QTabBar::tab:last:selected { margin-right: 0;} QTabBar::tab:only-one { margin: 0;}")
		#self.setStyleSheet("QTabBar { border: none; padding: 0px; }")
		
	def styleTab(self, index):
		tabButton = TabButton(self)
		self.setTabButton(index, QtGui.QTabBar.RightSide, tabButton)
		self.tabIndex.addTab((tabButton.id, tabButton)) #add tab to index
		tabButton.clicked.connect(self.__tabButtonPressed) #connect signal(emits tabButton.id) to handler
		self.log.debug('Adding Tab (%s, %s)'%(tabButton.id, index))
		
		return tabButton.id
		
	def __tabButtonPressed(self, id):
		print id
		tab = self.tabIndex.getTab(id)
		print tab
		self.tabCloseRequested.emit(tab)
		self.log.debug('tabButton triggered - (%s, %s)'%tab)
		return tab
		
	def removeTab(self, tabId):
		tab = self.tabIndex.removeTab(tabId)
		self.log.debug('Removed tab (%s, %s)'%tab)
		return tab
		
	def setTabDirty(self, tabId):
		id, tabButton = self.tabIndex.getTabButton(tabId)
		tabButton.setDirty()
	
	def setTabClean(self, tabId):
		id, tabButton = self.tabIndex.getTabButton(tabId)
		tabButton.setClean()
		
		
class TabButton(QtGui.QToolButton):

	clicked = QtCore.pyqtSignal(str)
	
	def __init__(self, *args):
		super(TabButton, self).__init__(*args)
		self.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.setIconSize(QtCore.QSize(15,15))
		self.setAutoRaise(True)
		self.id = uuid.uuid4().hex
		#Load Icons
		self.iconClean = QtGui.QIcon()
		self.iconClean.addFile('images\\check-green.svg', mode=QtGui.QIcon.Normal)
		self.iconClean.addFile('images\\x-green.svg', mode=QtGui.QIcon.Active)
		
		self.iconDirty = QtGui.QIcon()
		self.iconDirty.addFile('images\\check-red.svg', mode=QtGui.QIcon.Normal)
		self.iconDirty.addFile('images\\x-red.svg', mode=QtGui.QIcon.Active)
		
		#set Icon as clean on creation
		self.setClean()
		
		#setup actions
		self.buttonAction = QtGui.QAction(self)
		self.buttonAction.triggered.connect(self.activated)
		self.setDefaultAction(self.buttonAction)
		
		#clicked = QtCore.pyqtSignal(int)
		#print 'loaded'
		self.show()
		
	def setClean(self):
		self.setIcon(self.iconClean)
		
	def setDirty(self):
		self.setIcon(self.iconDirty)
		
	def activated(self, action):
		self.clicked.emit(self.id)
		
class FancyTabWidget(QtGui.QTabWidget):
	def __init__(self, *args):
		super(FancyTabWidget, self).__init__(*args)
		self.fancyTabBar = FancyTabBar()
		self.setTabBar(self.fancyTabBar)
		
		self.defaultTabWidth = 100
		self.setOptions()
		self.show()
	def setOptions(self):
		self.setTabShape(QtGui.QTabWidget.Triangular)
		#self.setStyleSheet("QTabBar::tab { min-width: 8ex; padding: 50px;} QTabBar::tab:selected { margin-left: -25px; margin-right: -25px;} QTabBar::tab:!selected { margin-top: 2px;}")
		self.setStyleSheet("QTabBar { border: 10px; padding: 5px; }")
		self.setStyleSheet("QTabWidget::pane {border: 1px solid #C2C7CB;}")
		
		self.setUsesScrollButtons(False)
		self.setMovable(True)
		self.setTabsClosable(True)

		#self.tabCloseRequested.connect(self.closeTab)
		
	def removeTab(self, tabId):
		if self.count() > 1:
			tab = self.fancyTabBar.tabIndex.getTab(tabId)
			self.removeTab(tab[1])
			self.setTabWidth()
		
	def setTabWidth(self):
		tabBarWidth = self.width()
		print tabBarWidth
		if not self.cornerWidget() == None:
			tabBarWidth = tabBarWidth - self.cornerWidget().width()

		perTab = int(tabBarWidth/self.count())
		
		if perTab < self.defaultTabWidth + 22:
			tabWidth = perTab-22
			
		else:
			tabWidth = self.defaultTabWidth
		
		self.setStyleSheet("QTabBar::tab { height: 24px; width: %spx; }"%str(tabWidth))
		
	def addTab(self, document):
		index = super(FancyTabWidget, self).addTab(document.codeEditor, document.basename)
		self.tabBar().styleTab(index)
		self.setTabWidth()
		self.setCurrentIndex(index)
		return index
		
			
class TabIndex(object):
	def __init__(self):
		self.tabs = SmartList()
		
	def addTab(self, tabButton):
		self.tabs.append(tabButton)
		#print str(tabButton)
		
	def removeTab(self, id):
		tab = self.getTab(id)
		if tab:
			return self.tabs.pop(tab[0])
		return None
		
	def moveTab(self, origin, destination):
		self.tabs.move(origin, destination)
		return destination
		
	def getTab(self, tabId):
		id, index = None, None
		#if tabId is str it is actually a id
		if isinstance(tabId, str):
			for id, tabButton in self.items:
				if id == tabId:
					index = self.tabs.index((id, tabButton))
		#if tabId is int its a index position
		if isinstance(tabId, int):
			index = tabId
			id = self.tabs.get(index)
			
		if id and index:
			return id, index
			
		return None
		
	def getTabButton(self, id):
		tab = self.getTab(id)
		if tab:
			return self.tabs[tab[1]]
		
		return None
		
		
class SmartList(object):
	def __init__(self, *args):
		self.items = []
		
	def __iter__(self):
		return self.items
		
	def append(self, item):
		self.items.append(item)
		#print 'appending item' + str(item)
		return len(self.items)-1
		
	def move(self, origin, dest):
		item = self.items.pop(origin)
		self.items.insert(dest, item)
		return dest
	
	def pop(self, index):
		return self.items.pop(index)
		
	def get(self, index):
		return self.items[index]