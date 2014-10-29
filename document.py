from highlighter import Highlighter
import editor
import os.path
from PyQt4 import QtGui, QtCore
from tabs import TabButton

class Document(QtGui.QWidget):
	def __init__(self, parent = None):
		
		QtGui.QWidget.__init__(self, parent)
			
		self.codeEditor = editor.CodeEditor(parent=self)
		self.formatter = Highlighter(self.codeEditor.document(), 'python')
		
		self.setupShortcuts()
		
		self.filename = None
		self.basename = 'new'
		
		#self.StatusIcon = TabButton()
			
	def loadFile(self):
		with open(self.filename, 'r') as file:
			text = file.read()
			print 'loaded'
			self.codeEditor.setPlainText(text)
			
	def saveFile(self):			
		with open(self.filename, 'w') as file:
			file.write(self.codeEditor.document().toPlainText())
			
	def setFilePath(self, filepath):
		print filepath
		self.filename = filepath
		self.basename = os.path.basename(str(self.filename))
		
	def Open(self, path = None):
		if not path:
			path = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
			if path == QtCore.QString():
				return False
				
		self.setFilePath(path)
		self.loadFile()
		return self
		
	def Save(self, path = None):
		if not path:
			if not self.filename:
				path = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
				if path == QtCore.QString():
					return False
			
			else:
				path = self.filename
				
		self.setFilePath(path)
		self.saveFile()
		#self.StatusIcon.setClean()
		return self
		
	def setupShortcuts(self):
		shortcuts = {
			'open':	['CTRL+O', self.parent().loadFile],
			'save':	['CTRL+S', self.Save], 
			'new':	['CTRL+N', self.parent().newFile],
					}
		
		self.shortcuts = {}
		
		for label, options in shortcuts.iteritems():
			shortcut = QtGui.QShortcut(options[0], self.codeEditor)
			self.connect(shortcut, QtCore.SIGNAL('activated()'), options[1])
			self.shortcuts[label] = shortcut
			
	def updateDirty(self):
		#self.StatusIcon.setDirty()
		return True
			
			
			