from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import os
import maya.cmds as cmds
from subprocess import Popen

class ImportWidget(QtWidgets.QWidget):
    
    file_ITEMS = os.listdir('F:/RePath_Pipe/PROJECT/02_PRODUCTION')
    
    __ROOT = 'F:/RePath_Pipe/PROJECT/02_PRODUCTION/'
    
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
        self.last_list_wdg = QtWidgets.QListWidget()
        
        for item in self.file_ITEMS:
            list_wdg_item = QtWidgets.QListWidgetItem(item)
            self.file_list_wdg.addItem(list_wdg_item)

        self.import_lbl = QtWidgets.QLabel('Import Mode')
        self.import_mode = QtWidgets.QRadioButton('Import')
        self.import_mode.setChecked(True)
        self.ref_mode = QtWidgets.QRadioButton('Reference')

        self.lastWIP = QtWidgets.QRadioButton('Import last WIP scene')
        self.publish = QtWidgets.QRadioButton('Import publish scene')
        self.publish.setChecked(True)
        
        self.importInScene_btn = QtWidgets.QPushButton('Import into this scene')
        self.openInScene_btn = QtWidgets.QPushButton('Open this scene')
        self.openInMaya_btn = QtWidgets.QPushButton('Open in new maya scene')

    
    def create_layout(self):
        
        master_layout = QtWidgets.QVBoxLayout(self)
        main_layout = QtWidgets.QHBoxLayout(self)
        wipP_layout = QtWidgets.QHBoxLayout(self)
        modes_layout = QtWidgets.QVBoxLayout(self)
        import_layout = QtWidgets.QHBoxLayout(self)
        buttons_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.file_list_wdg)
        main_layout.addStretch()
        main_layout.addWidget(self.type_list_wdg)
        main_layout.addStretch()
        main_layout.addWidget(self.dep_list_wdg)
        main_layout.addStretch()
        main_layout.addWidget(self.last_list_wdg)
        main_layout.addStretch()
        
        wip_gb = QtWidgets.QGroupBox('')
        import_gb = QtWidgets.QGroupBox('')

        wipP_layout.addWidget(self.lastWIP)
        wipP_layout.addWidget(self.publish)
        wip_gb.setLayout(wipP_layout)

        import_layout.addWidget(self.import_lbl)
        
        modes_layout.addWidget(self.import_mode)
        modes_layout.addWidget(self.ref_mode)
        import_layout.addLayout(modes_layout)
        import_gb.setLayout(import_layout)

        buttons_layout.addWidget(self.importInScene_btn)
        buttons_layout.addWidget(self.openInScene_btn)
        buttons_layout.addWidget(self.openInMaya_btn)
        
        
        master_layout.addLayout(main_layout)
        master_layout.addWidget(wip_gb)
        master_layout.addWidget(import_gb)
        master_layout.addLayout(buttons_layout)
        

    def create_connections(self):
        self.file_list_wdg.itemClicked.connect(self.update_fList)
        self.type_list_wdg.itemClicked.connect(self.update_aList)
        self.dep_list_wdg.itemClicked.connect(self.update_depList)
        self.importInScene_btn.clicked.connect(self.importInThisScene)
        self.openInMaya_btn.clicked.connect(self.openInNewScene)
        self.openInScene_btn.clicked.connect(self.openInThisScene)

    def update_fList(self, item):
        self.type_list_wdg.clear()
        self.dep_list_wdg.clear()
        self.last_list_wdg.clear()
        currentItem = item.text()
        searchPath = self.__ROOT + currentItem 
        type_ITEMS = os.listdir(searchPath)
        
        for each in type_ITEMS:
            type_item = QtWidgets.QListWidgetItem(each)
            self.type_list_wdg.addItem(type_item)

        

    def update_aList(self, item):
        self.dep_list_wdg.clear()
        self.last_list_wdg.clear()
        
        file_list_item = self.file_list_wdg.currentItem().text()
        currentItem = item.text()
        searchPath = self.__ROOT + file_list_item + '/' + currentItem 
        dep_ITEMS = os.listdir(searchPath)
        
        for each in dep_ITEMS:
            dep_item = QtWidgets.QListWidgetItem(each)
            self.dep_list_wdg.addItem(dep_item)
    
    def update_depList(self, item):
        self.last_list_wdg.clear()
        file_list_item = self.file_list_wdg.currentItem().text()
        type_list_item = self.type_list_wdg.currentItem().text()
        currentItem = item.text()
        searchPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + currentItem
        last_ITEMS = os.listdir(searchPath)
        
        for each in last_ITEMS:
            lst_item = QtWidgets.QListWidgetItem(each)
            self.last_list_wdg.addItem(lst_item)

    def importInThisScene(self):
        importOrReference = self.import_mode.isChecked()
        wip_Check = self.lastWIP.isChecked()

        file_list_item = self.file_list_wdg.currentItem().text()
        type_list_item = self.type_list_wdg.currentItem().text()
        dep_list_item = self.dep_list_wdg.currentItem().text()
        last_list_item = self.last_list_wdg.currentItem().text()
        
        if importOrReference == True:
            if wip_Check == True:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/WIP'
                filePath = os.listdir(goodPath)
                ### cambiar a la ultima version , busqueda por ultima modificacion (chapuzero pero funciona)
                lastModFile = []
                finalFileName = []
                timeList =[]
                for each in filePath:
                    mTime = os.path.getmtime(goodPath + '/' + each)
                    lastModFile.append([each, mTime])
                
                for eachTime in lastModFile:
                    timeList.append(eachTime[1])
                goodfiletime = float(max(timeList))
                for item in lastModFile:
                    if goodfiletime in item:
                        finalFileName.append(item[0])
                        print(item[0])
                cmds.file( goodPath + '/' + finalFileName[0] , i=True )
                print(goodPath + '/' + finalFileName[0])
            else:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/PUBLISH'
                filePath = os.listdir(goodPath)
                cmds.file( goodPath + '/' + filePath[0] , i=True )
                print(goodPath + '/' + filePath[0])
        else:
            if wip_Check == True:
                print('wip es true')
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/WIP'
                filePath = os.listdir(goodPath)
                ### cambiar a la ultima version , busqueda por ultima modificacion (chapuzero pero funciona)
                lastModFile = []
                finalFileName = []
                timeList =[]
                for each in filePath:
                    mTime = os.path.getmtime(goodPath + '/' + each)
                    lastModFile.append([each, mTime])
                
                for eachTime in lastModFile:
                    timeList.append(eachTime[1])
                goodfiletime = float(max(timeList))
                for item in lastModFile:
                    if goodfiletime in item:
                        finalFileName.append(item[0])
                        print(goodPath + '/' + item[0])
                cmds.file( goodPath + '/' + finalFileName[0] , r=True, ns=finalFileName[0] )
                print(goodPath + '/' + finalFileName[0])
            else:
                # print('wip es false')
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/PUBLISH'
                
                filePath = os.listdir(goodPath)
                cmds.file( goodPath + '/' + filePath[0], r=True )
                print(filePath)
        

    def openInThisScene(self):
        importOrReference = self.import_mode.isChecked()
        wip_Check = self.lastWIP.isChecked()
        
        file_list_item = self.file_list_wdg.currentItem().text()
        type_list_item = self.type_list_wdg.currentItem().text()
        dep_list_item = self.dep_list_wdg.currentItem().text()
        last_list_item = self.last_list_wdg.currentItem().text()


        if importOrReference == True:
            if wip_Check == True:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/WIP'
                filePath = os.listdir(goodPath)
                ### cambiar a la ultima version , busquedal por ultima modificacion (chapuzero pero funciona)
                lastModFile = []
                finalFileName = []
                timeList =[]
                for each in filePath:
                    mTime = os.path.getmtime(goodPath + '/' + each)
                    lastModFile.append([each, mTime])
                
                for eachTime in lastModFile:
                    timeList.append(eachTime[1])
                goodfiletime = float(max(timeList))
                for item in lastModFile:
                    if goodfiletime in item:
                        finalFileName.append(item[0])
                        print(item[0])
                cmds.file( goodPath + '/' + finalFileName[0] , o=True, force=True)
            else:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/PUBLISH'
                filePath = os.listdir(goodPath)
                cmds.file( goodPath + '/' + filePath [0], o=True, force=True)
        else:
            if wip_Check == True:
                print('wip es true')
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/WIP'
                filePath = os.listdir(goodPath)
                ### cambiar a la ultima version , busqueda por ultima modificacion (chapuzero pero funciona)
                lastModFile = []
                finalFileName = []
                timeList =[]
                for each in filePath:
                    mTime = os.path.getmtime(goodPath + '/' + each)
                    lastModFile.append([each, mTime])
                
                for eachTime in lastModFile:
                    timeList.append(eachTime[1])
                goodfiletime = float(max(timeList))
                for item in lastModFile:
                    if goodfiletime in item:
                        finalFileName.append(item[0])
                        print(goodPath + '/' + item[0])
                cmds.file( goodPath + '/' + finalFileName[0] , r=True, ns=finalFileName[0] )
                print(goodPath + '/' + finalFileName[0])
            else:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/PUBLISH'
                filePath = os.listdir(goodPath)
                cmds.file(new=True, force=True) 
                cmds.file( goodPath + '/' + filePath[0], r=True, ns=finalFileName[0])
                
            

    def openInNewScene(self):
        importOrReference = self.import_mode.isChecked()
        wip_Check = self.lastWIP.isChecked()
        
        file_list_item = self.file_list_wdg.currentItem().text()
        type_list_item = self.type_list_wdg.currentItem().text()
        dep_list_item = self.dep_list_wdg.currentItem().text()
        last_list_item = self.last_list_wdg.currentItem().text()


        if importOrReference == True:
            if wip_Check == True:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/WIP'
                filePath = os.listdir(goodPath)
                ### cambiar a la ultima version , busquedal por ultima modificacion (chapuzero pero funciona)
                lastModFile = []
                finalFileName = []
                timeList =[]
                for each in filePath:
                    mTime = os.path.getmtime(goodPath + '/' + each)
                    lastModFile.append([each, mTime])
                
                for eachTime in lastModFile:
                    timeList.append(eachTime[1])
                goodfiletime = float(max(timeList))
                for item in lastModFile:
                    if goodfiletime in item:
                        finalFileName.append(item[0])
                        print(item[0])
                Popen(r"C:\Program Files\Autodesk\Maya2018\bin\maya.exe -file {}".format(goodPath + '/' + finalFileName[0]))
            else:
                goodPath = self.__ROOT + file_list_item + '/' + type_list_item + '/' + dep_list_item + '/' + last_list_item + '/PUBLISH'
                filePath = os.listdir(goodPath)
                Popen(r"C:\Program Files\Autodesk\Maya2018\bin\maya.exe -file {}".format(goodPath + '/' + filePath [0]))
        else:
            print("Can't reference in new maya scene, sorry :(")


