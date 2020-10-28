from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import os

class ImportWidget(QtWidgets.QWidget):
    file_ITEMS = os.listdir('F:/RePath_Pipe/PROJECT/02_PRODUCTION')
    
    def __init__(self, parent=None):
        super(ImportWidget, self).__init__(parent)
        #widgets 
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    def create_widgets(self):
        
        self.file_list_wdg = QtWidgets.QListWidget()
        self.type_list_wdg = QtWidgets.QListWidget()
        self.dep_list_wdg = QtWidgets.QListWidget()
        
        for item in self.file_ITEMS:
            list_wdg_item = QtWidgets.QListWidgetItem(item)
            self.file_list_wdg.addItem(list_wdg_item)
    
    def create_layout(self):

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.file_list_wdg)
        main_layout.addStretch()
        main_layout.addWidget(self.type_list_wdg)
        main_layout.addStretch()
        main_layout.addWidget(self.dep_list_wdg)
        main_layout.addStretch()

    def create_connections(self):
        self.file_list_wdg.itemClicked.connect(self.update_fList)
        self.type_list_wdg.itemClicked.connect(self.update_aList)
        

    def update_fList(self, item):
        self.type_list_wdg.clear()
        self.dep_list_wdg.clear()
        currentItem = item.text()
        searchPath = r'F:/RePath_Pipe/PROJECT/02_PRODUCTION/' + currentItem 
        type_ITEMS = os.listdir(searchPath)
        
        for each in type_ITEMS:
            type_item = QtWidgets.QListWidgetItem(each)
            self.type_list_wdg.addItem(type_item)

        print(a_list)

    def set_mierda(self, item):
        self.dep_list_wdg.clear()
        
        file_list_item = self.file_list_wdg.currentItem().text()
        currentItem = item.text()
        searchPath = r'F:/RePath_Pipe/PROJECT/02_PRODUCTION/' + file_list_item + '/' + currentItem 
        dep_ITEMS = os.listdir(searchPath)
        
        for each in dep_ITEMS:
            dep_item = QtWidgets.QListWidgetItem(each)
            self.dep_list_wdg.addItem(dep_item)

        # print(searchPath)