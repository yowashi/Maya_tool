from maya import cmds
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

UI_FIlE = r"C:\Users\hinzy\Desktop\Program\UI\visible_tool.ui"

class Visible_Tool(MayaQWidgetBaseMixin,QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Visible_Tool,self).__init__( *args, **kwargs)

        self.widget = QUiLoader().load(UI_FIlE)
        self.setWindowTitle('Visible Tool')
        self.setCentralWidget(self.widget)
        self.widget.visibile_off_btn.clicked.connect(self.visible_off_controller)
        self.widget.visible_on_btn.clicked.connect(self.visible_on_controller)


    def add_visibility_geo_list(self):
        all_geo = cmds.ls(typ='shape')
        ROPGEO_in = [s for s in all_geo if 'ROPGEO' in s]
        return ROPGEO_in
    
    def visible_on_controller(self):
        visible_list = self.add_visibility_geo_list()
        for visible_on in visible_list:
            cmds.setAttr(visible_on + '.primaryVisibility',1)

    def visible_off_controller(self):
        visible_list = self.add_visibility_geo_list()
        for visible_off in visible_list:
            cmds.setAttr(visible_off + '.primaryVisibility',0)

def main():
    window = Visible_Tool()
    window.show()

if __name__ == '__main__':
    main()