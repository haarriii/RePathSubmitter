from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets


class ImportWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ImportWidget, self).__init__(parent)
        #widgets 
        self.create_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        self.optimizeScene = QtWidgets.QPushButton("Optimize Scene")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.optimizeScene)
        layout.addWidget(QtWidgets.QPushButton("Button 02"))
        layout.addWidget(QtWidgets.QPushButton("Button 03"))
        layout.addWidget(QtWidgets.QPushButton("Button 04"))
        
    def create_connections(self):
        pass

    def ff(self):
        print('hahah me riio en tu cara')