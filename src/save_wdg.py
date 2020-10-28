from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import maya.cmds as cmds
import os
from datetime import date, datetime
import getpass

class SaveWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SaveWidget, self).__init__(parent)
        #widgets 
        self.create_widgets()
        self.create_connections()
        
    def create_widgets(self):
        
        main_layout = QtWidgets.QVBoxLayout(self)
        self.optimizeScene = QtWidgets.QPushButton("Optimize Scene")
        self.modelChecker = QtWidgets.QPushButton("Model Cheker")
        
        buttons_layout = QtWidgets.QHBoxLayout(self)
        name_layout = QtWidgets.QHBoxLayout(self)
        combo_layout = QtWidgets.QHBoxLayout(self)
        radio_layout= QtWidgets.QHBoxLayout(self)
        buttons_layout.addWidget(self.modelChecker)
        buttons_layout.addWidget(self.optimizeScene)
        buttons_layout.addWidget(QtWidgets.QPushButton("Button 03"))
        
        
        
        mainType = ['ASSETS', 'SHOTS']
        fileType = ['CHAR','ELEMS','LOCATION','PROPS', 'VEGETATION']
        departmentType = ['01_SCLUPT', '02_MODEL', '03_RIG', '04_TEXTURING', '06_LOOKDEV']
        shotName = ['SHOT0010', 'SHOT0020', 'SHOT0030']
       

        self.maintype_cb = QtWidgets.QComboBox()
        
        for each in mainType:
            self.maintype_cb.addItem(each)
        
        self.type_cb = QtWidgets.QComboBox()
        
        for each in fileType:
            self.type_cb.addItem(each)
        
        self.dep_cb = QtWidgets.QComboBox()
        
        for each in departmentType:
            self.dep_cb.addItem(each)
        
        self.maintype_cb.currentIndexChanged.connect(self.setMainType)

        self.simpleLBL = QtWidgets.QLabel('Asset Name:')
        self.fileName = QtWidgets.QLineEdit()

        self.prod_wip = QtWidgets.QRadioButton('WIP')
        self.prod_wip.setChecked(True)
        
        self.prod_publish = QtWidgets.QRadioButton('PUBLISH')
        
        self.save_btn = QtWidgets.QPushButton('Save')

        main_layout.addLayout(buttons_layout)
        
        combo_layout.addWidget(self.maintype_cb)
        combo_layout.addWidget(self.type_cb)
        combo_layout.addWidget(self.dep_cb)
        
        main_layout.addLayout(combo_layout)
        
        name_layout.addWidget(self.simpleLBL)
        name_layout.addWidget(self.fileName)
        main_layout.addLayout(name_layout)

        radio_layout.addWidget(self.prod_wip)
        radio_layout.addWidget(self.prod_publish)
        main_layout.addLayout(radio_layout)
    
        main_layout.addWidget(self.save_btn)

    
    def create_connections(self):
        self.optimizeScene.clicked.connect(self.sendprint)
        self.modelChecker.clicked.connect(self.modelCheckInfo)
        self.save_btn.clicked.connect(self.save_scene)

    def modelCheckInfo(self):
        from modelChecker_UI import modelCheckerUI
        modelCheckerUI.show_UI()
    
    def sendprint(self):
        import maya.mel as mel
        mel.eval("cleanUpScene 1")

    def setMainType(self):
        currentIndex = self.maintype_cb.currentIndex()
        print(currentIndex)
        if currentIndex == 0:
            self.type_cb.setEnabled(True)
            self.prod_publish.setEnabled(True)
            self.prod_wip.setEnabled(True)
            self.fileName.setEnabled(True)
            self.dep_cb.setEnabled(True)
        else:
            self.type_cb.setEnabled(False)
            self.prod_publish.setEnabled(False)
            self.prod_wip.setEnabled(False)
            self.fileName.setEnabled(False)
            self.dep_cb.setEnabled(False)
    
    def save_scene(self):
        fileMainPath = self.maintype_cb.currentText()
        assetType = self.type_cb.currentText()
        assetName = self.fileName.text()
        depType = self.dep_cb.currentText()

        if fileMainPath == 'ASSETS':
            self.fileTypePath = 'ASSETS'
        else:
            self.fileTypePath = 'SHOTS'
        
        if assetType == 'CHARS':
            self.assetTypeX = 'CHAR_'
        elif assetType == 'ELEMS':
            self.assetTypeX = 'ELEM_'
        elif assetType == 'LOCATIONS':
            self.assetTypeX = 'LOC_'
        elif assetType == 'PROPS':
            self.assetTypeX = 'PRP_'
        elif assetType == 'VEGETATIONS':
            self.assetTypeX = 'VGT_'
        else:
            print('Error en el tipo de archivo en "type_cb"(ComboBox)')

        if self.prod_wip.isChecked() == True:
            self.publish = 'WIP'
        else:
            self.publish = 'PUBLISH'
        self.goodName = self.assetTypeX + assetName + '_' + self.publish
        rootPath = r'F:/RePath_Pipe/PROJECT/02_PRODUCTION/'
        self.goodNamedFilePath = rootPath + self.fileTypePath + '/' + assetType + '/' + self.assetTypeX + assetName + '/' + depType + '/' + self.publish
        if not os.path.exists(self.goodNamedFilePath):
            os.makedirs(self.goodNamedFilePath)
        self.scene_name = self.goodNamedFilePath + '/' + self.goodName 
        cmds.file( rename= self.scene_name)
        cmds.file( save=True, type='mayaAscii')

        self.outputlog()


    def outputlog(self):
        log = r'F:/RePath_Pipe/PROJECT/00_RESOURCES/submitter_log.txt'
        today = date.today()
        now = datetime.now()
        scene_name = cmds.file(q=True, sn=True)
        scene_path = str(scene_name)
        current_time = now.strftime("%H:%M:%S")
        author = getpass.getuser()
        with open(log, "a+") as file_object:
            # Append text at the end of file
            file_object.write('\n{0} upload {1} at {2} {3}'.format(author,scene_path, today,current_time))