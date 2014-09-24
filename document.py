from highlighter import Highlighter
import editor
import os.path
from PyQt4 import QtGui, QtCore

class Document(QtGui.QWidget):
	def __init__(self, parent = None):
		
		QtGui.QWidget.__init__(self, parent)
			
		self.codeEditor = editor.CodeEditor()
		self.formatter = Highlighter(self.codeEditor.document(), 'python')
		
		self.setupShortcuts()
		
		self.filename = None
		self.basename = 'new'
			
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
		
		self.setFilePath(path)
		self.loadFile()
		return self
		
	def Save(self, path = None):
		if not path:
			if not self.filename:
				path = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
			
			else:
				path = self.filename
				
		self.setFilePath(path)
		self.saveFile()		
		return self
		
	def setupShortcuts(self):
		list = {
			'open':	['CTRL+O',self.Save],
			'save':	['CTRL+S',self.parent().loadFile], 
			'new':	['CTRL+N', self.parent().newFile],
					}
		
		self.shortcuts = {}
		
		for label, options in list.iteritems():
			shortcut = QtGui.QShortcut(options[0], self.codeEditor)
			self.connect(shortcut, QtCore.SIGNAL('activated()'), options[1])
			self.shortcuts[label] = shortcut
			
			
			