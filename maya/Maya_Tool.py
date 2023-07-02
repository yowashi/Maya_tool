from maya import cmds
from maya import OpenMaya
import os
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

UI_FILE = r"C:\Users\hinzy\Desktop\program\maya\Maya_Tool.ui"


class IK_ControllerWindow(MayaQWidgetBaseMixin,QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(IK_ControllerWindow,self).__init__(*args, **kwargs) 

        self.widget = QUiLoader().load(UI_FILE)
        self.setWindowTitle("IK_Controller_Tool")
        self.setCentralWidget(self.widget)
        self.widget.create_aim_con_btn.clicked.connect(self.create_aim_ik_controller)
        self.widget.create_arm_con_btn.clicked.connect(self.create_arm_ik_controller)
        self.widget.create_leg_con_btn.clicked.connect(self.create_leg_ik_controller)
        self.widget.create_hand_con_btn.clicked.connect(self.create_hand_controller)
        self.widget.create_spine_con_btn.clicked.connect(self.create_spine_controller)
        
        #controllerとjntは別階層して管理をしやすくする。
        #余裕があったらIK/FK両方対応ツールを開発する。
        #始めはIKオンリー
    def create_arm_ik_controller(self):
        """
        腕にIK/FKコントローラーを生成して、手首、肩にコントローラー、肘にポールベクター、手に表情用コントローラーを作成して設置する。
        jointは基本1軸、コントローラーに値が入る。
        手の表情ドリブンの登録は手動設定。
        """
        print("arm_controller")
        

    def create_aim_ik_controller(self):
        pass

    def create_leg_ik_controller(self):
        pass

    def create_hand_controller(self):
        pass

    def create_spine_controller(self):
        """
        ref_jntにreference(curves)を設定してSpine_contを親子付けしていく
        controllerとjntは別階層して管理をしやすくする。
        """
        pass

def main():
    window = IK_ControllerWindow()
    window.show()

if __name__ == '__main__':
    main()