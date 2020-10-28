from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import sys

import getpass

import maya.cmds as cmds

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMayaUI as omui




p = r'Z:/TFG/Sripts/RepathSubmitter/src'
if not p in sys.path:
    sys.path.append(p)

from tab_widgets import CustomTabWidget
from save_wdg import SaveWidget
from import_wdg import ImportWidget



def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class RepathSubmitterDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(RepathSubmitterDialog, self).__init__(parent)
        self.setObjectName('REPATH_SUBMITTER_UI')
        self.setWindowTitle("RePath Submitter")
        self.setMinimumWidth(500)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.titleimage = QtWidgets.QLabel('RePath Submitter')
        imagePath = r'Z:/TFG/Sripts/RepathSubmitter/src/re_path.png'
        image = QtGui.QPixmap(imagePath)
        self.titleimage.setPixmap(image)
        self.titleimage.setAlignment(QtCore.Qt.AlignCenter)
        
        self.workingperson = QtWidgets.QLabel(getpass.getuser())
        self.workingperson.setAlignment(QtCore.Qt.AlignCenter)
        

        self.save_wdg = SaveWidget()
        self.import_wdg = ImportWidget()

        self.tab_widget = CustomTabWidget()
        self.tab_widget.addTab(self.save_wdg, "Save")
        self.tab_widget.addTab(self.import_wdg, "Import")


    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.titleimage)
        form_layout.addRow("Working:", self.workingperson)
    

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.tab_widget)
        

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        pass
    
    
    


if __name__ == "__main__":

    try:
        repath_dialog.close() # pylint: disable=E0601
        repath_dialog.deleteLater()
    except:
        pass

    repath_dialog = RepathSubmitterDialog()
    repath_dialog.show(dockable=True, area="right", floating=False)
