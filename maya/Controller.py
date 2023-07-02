from maya import cmds
from maya import OpenMaya
import os
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

UI_FILE = r"C:\Users\hinzy\Desktop\Program\UI\Controler.ui"


class IK_ControllerWindow(MayaQWidgetBaseMixin,QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(IK_ControllerWindow,self).__init__(*args, **kwargs) 

        self.widget = QUiLoader().load(UI_FILE)
        self.setWindowTitle("IK_Controller_Tool")
        self.setCentralWidget(self.widget)
        self.widget.aim_controller_btn.clicked.connect(self.create_aim_ik_controller)
        self.widget.arm_controller_btn.clicked.connect(self.create_arm_ik_controller)
        self.widget.leg_controller_btn.clicked.connect(self.create_leg_ik_controller)
        self.widget.hand_controller_btn.clicked.connect(self.create_hand_controller)
        
        #controllerとjntは別階層して管理をしやすくする。
        #余裕があったらIK/FK両方対応ツールを開発する。
        #始めはIKオンリー
        #回転は基本z軸、orinetjoint_front_Z
        """
        腕にコントローラーを生成して、手首、肩にコントローラー、肘にポールベクター、手に表情用コントローラーを作成して設置する。
        jointは基本1軸、コントローラーに値が入る。
        手の表情ドリブンの登録は手動設定。
        """
    def create_arm_ik_controller(self):
        cheack = cmds.ls('left_hand_ikHandle')
        if not cheack:
            joint_name = "left_shoulder_jnt|left_fore_arm_jnt"
            preferred_angle = -90
            self.set_joint_preferred_angle(joint_name,preferred_angle)
            cmds.ikHandle(n='left_hand_ikHandle',sol='ikRPsolver',sj="left_shoulder_jnt",ee="left_palm_jnt",s='sticky')
            cmds.ikHandle(n='left_shoulder_ikHandle',sol='ikRPsolver',sj="left_clavicle_jnt",ee="left_shoulder_jnt",s='sticky')
            cmds.rename('effector1', 'left_hand_ikHandle_effector')
            cmds.rename('effector2', 'left_shoulder_effector')
            move_obj = cmds.circle(n='left_arm_CTR',r=5)
            target_obj = cmds.ls('left_hand_ikHandle',typ='ikHandle')
            self.move_select_object_point(move_obj,target_obj)
            cmds.rotate(0,'90deg',0,move_obj)
            cmds.makeIdentity('left_arm_CTR',a=True)
            cmds.parent('left_hand_ikHandle','left_arm_CTR')
            shoulder_CTR = cmds.circle(n='left_shoulder_CTR', r = 8)
            move_to_obj = cmds.ls('left_shoulder_ikHandle',typ='ikHandle')
            self.move_select_object_point(shoulder_CTR,move_to_obj)
            cmds.rotate(0,'90deg',0,shoulder_CTR)
            cmds.makeIdentity('left_shoulder_CTR',a=True)
            cmds.parent('left_shoulder_ikHandle','left_shoulder_CTR',)
            move_obj = cmds.spaceLocator(n='left_elbow_CTR')
            target_jnt = cmds.ls('left_fore_arm_jnt',typ='joint')
            self.move_select_object_point(move_obj,target_jnt)
            cmds.move(0,0,-10,move_obj,r=True,os=True,wd=True)
            cmds.poleVectorConstraint('left_elbow_CTR',target_obj)
            cmds.parent('left_elbow_CTR','left_arm_CTR')
            serch_strings = 'hand'
            par_list = self.list_parent_constraint(serch_strings)
            print(par_list)
            self.create_circle_contorller(par_list)


            

        else:
            self.error_window()

    def create_aim_ik_controller(self):
        pass

    def create_leg_ik_controller(self):
        pass

    def create_hand_controller(self):
        pass
        """
        ref_jntにreference(curves)を設定してSpine_contを親子付けしていく
        controllerとjntは別階層して管理をしやすくする。
        """

        #ジョイント優先角設定関数
    def set_joint_preferred_angle(self, joint_name, preferred_angle):
        cmds.select(joint_name)
        cmds.setAttr(joint_name +'.rotateY',preferred_angle)
        cmds.joint(e=True, spa=True,ch=True)
        cmds.setAttr(joint_name + '.rotateY',0)

        #指定オブジェクトに移動する関数
    def move_select_object_point(self,move_obj,target_obj):
        for target in target_obj:
            target_position = cmds.xform(target_obj, query=True, translation=True, worldSpace=True)
            #rotate_position = cmds.xform(target_obj,query = True, ro=True,worldSpace = True)
            cmds.xform(move_obj,translation=target_position, worldSpace=True)

        #エラーウィンドウ表示
    def error_window(self):
        window = cmds.window(t='error_window',widthHeight=(400,50))
        cmds.columnLayout( adjustableColumn=True )
        cmds.text('Already create IK_Controler',bgc=(1,1,1))
        cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
        cmds.setParent( '..' )
        cmds.showWindow( window )

        #指定文字列を含むjointのリストを返す
    def list_parent_constraint(self,serch_strings):
        all_nodes =cmds.ls(typ='joint')
        search_list = []
        for constraint in all_nodes:
            if serch_strings in constraint:
                search_list.append(constraint)
        return search_list
    
        #リストの分だけCTRを作って移動させる
    def create_circle_contorller(self,par_list):
        for circle in par_list:
            CTR_name = circle + '_CTR'
            move_obj = cmds.circle(n = CTR_name ,r=1)
            self.move_select_object_point(move_obj,[circle])
            #cmds.rotate(0,'90deg',0,move_obj)
            #cmds.matchTransform(move_obj,[circle],rot=True)
            #cmds.makeIdentity(move_obj,a=True)



def main():
    window = IK_ControllerWindow()
    window.show()

if __name__ == '__main__':
    main()