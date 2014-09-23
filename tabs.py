from PyQt4 import QtGui, QtCore

class FramelessTabWidget(QtGui.QWidget):
	pass
	
class FancyTabBar(QtGui.QTabBar):
	def __init__(self, parent=None):
		super(FancyTabBar, self).__init__(parent)
		self.tabCount = 1
		self.setStyleSheet("""
			QTabBar::tab { 
				height: 24px; 
				margin-left: -4px; 
				margin-right: -4px; 
				padding-left: 15px; 
				padding-right: 15px;
			}
			QTabBar::tab:only-one {
				margin: 0px;
			}
			QTabBar::tab:first { 
				margin-left: 0px;
			}
			""")
		#self.setStyleSheet("QTabWidget::tab-bar {left: 5px;} QTabBar::tab:!selected { margin-top: 2px;} QTabBar::tab:selected {margin-left: -4px; margin-right: -4px;} QTabBar::tab:first:selected { margin-left: 0;} QTabBar::tab:last:selected { margin-right: 0;} QTabBar::tab:only-one { margin: 0;}")
		#self.setStyleSheet("QTabBar { border: none; padding: 0px; }")
			
		
class TabButton(QtGui.QToolButton):
	def __init__(self, *args):
		super(TabButton, self).__init__(*args)
		self.setStyleSheet("QToolButton { border: none; padding: 0px; }")
		self.setIconSize(QtCore.QSize(16,16))
		self.setAutoRaise(True)
		
		#Load Icons
		self.iconClean = QtGui.QIcon()
		self.iconClean.addFile('images/check-green.svg', mode=QtGui.QIcon.Normal)
		self.iconClean.addFile('images/x-green.svg', mode=QtGui.QIcon.Active)
		
		self.iconDirty = QtGui.QIcon()
		self.iconDirty.addFile('images/check-red.svg', mode=QtGui.QIcon.Normal)
		self.iconDirty.addFile('images/x-red.svg', mode=QtGui.QIcon.Active)
		
		self.setIcon(self.iconDirty)
		
	def setClean(self):
		self.setIcon(self.iconClean)
		
	def setDirty(self):
		self.setIcon(self.iconDirty)
		
	

	