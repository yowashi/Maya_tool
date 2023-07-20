from maya import cmds
from maya import OpenMaya
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

            cmds.mirrorJoint('left_clavicle_jnt',myz=True,mb=True, sr=('left','right'))

            left_arm_handle_name = 'left_arm_CTR'
            left_CTR_obj = cmds.circle(n=left_arm_handle_name,r=5)
            left_target_obj = cmds.ls('left_hand_ikHandle',typ='ikHandle')
            self.create_parent_circle(left_arm_handle_name,left_CTR_obj,left_target_obj)

            right_arm_handle_name = 'right_arm_CTR'
            right_CTR_obj = cmds.circle(n = right_arm_handle_name, r=5)
            right_target_obj = cmds.ls('right_hand_ikHandle',typ='ikHandle')
            self.create_parent_circle(right_arm_handle_name,right_CTR_obj,right_target_obj)

            left_shoulder_handle_name = 'left_shoulder_CTR'
            left_shoulder_CTR = cmds.circle(n= left_shoulder_handle_name, r = 8)
            left_move_to_obj = cmds.ls('left_shoulder_ikHandle',typ='ikHandle')
            self.create_parent_circle(left_shoulder_handle_name,left_shoulder_CTR,left_move_to_obj)

            right_shoulder_handle_name = 'right_shoulder_CTR'
            right_shoulder_CTR = cmds.circle(n= right_shoulder_handle_name, r = 8)
            right_move_to_obj = cmds.ls('right_shoulder_ikHandle',typ='ikHandle')
            self.create_parent_circle(right_shoulder_handle_name,right_shoulder_CTR,right_move_to_obj)

            left_target_ctr = 'left_elbow_CTR'
            left_move_obj = cmds.spaceLocator(n= left_target_ctr)
            left_target_jnt = cmds.ls('left_fore_arm_jnt',typ='joint')
            self.create_polevector(left_target_ctr,left_move_obj,left_target_jnt,left_target_obj,left_arm_handle_name)

            right_target_ctr = 'right_elbow_CTR'
            right_move_obj = cmds.spaceLocator(n= right_target_ctr)
            right_target_jnt = cmds.ls('right_fore_arm_jnt',typ='joint')
            self.create_polevector(right_target_ctr,right_move_obj,right_target_jnt,right_target_obj,right_arm_handle_name)

            serch_strings = 'hand'
            par_list = self.list_parent_constraint(serch_strings)
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
        
        #IKコントローラー作成
    def create_IK_controller(self,create_string,start_jnt,end_jnt):
        cmds.ikHandle(n=create_string + '_ikHandle', sol='ikRPsolver', sj=start_jnt, ee=end_jnt, s='sticky')
        cmds.rename('effector1',create_string + 'ikHandle_effector')

        #指定オブジェクトに移動する関数
    def move_select_object_point(self,move_obj,target_obj):
        for target in target_obj:
            target_position = cmds.xform(target_obj, query=True, translation=True, worldSpace=True)
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
    
        #リストの分だけCTRを作って移動させた後、回転軸をjintに合わせる。
    def create_circle_contorller(self,par_list):
        conts_node = []
        for circle in par_list:
            CTR_name = circle + '_CTR'
            move_obj = cmds.circle(n = CTR_name ,r=1,nr=(1,0,0))
            move_obj_str = cmds.ls(CTR_name)
            print(move_obj_str[0])
            self.move_select_object_point(move_obj,[circle])
            cmds.orientConstraint([circle],move_obj)
            cmds.orientConstraint([circle],move_obj,e=True,rm=True)
        
        #作成したコントローラーを指定objに移動しフリーズした後ペアレントする
    def create_parent_circle(self,handle_name,move_obj,target_obj):
        self.move_select_object_point(move_obj,target_obj)
        cmds.rotate(0,'90deg',0, move_obj)
        cmds.makeIdentity(handle_name, a=True)
        cmds.parent(target_obj,handle_name)

        #ポールベクターを作成する
    def create_polevector(self,target_ctr,move_obj,target_jnt,target_obj,handle_name):
        self.move_select_object_point(move_obj,target_jnt)
        cmds.move(0,0,-10,move_obj,r=True,os=True,wd=True)
        cmds.poleVectorConstraint(target_ctr,target_obj)
        cmds.parent(target_ctr,handle_name)

def main():
    window = IK_ControllerWindow()
    window.show()

if __name__ == '__main__':
    main()


   