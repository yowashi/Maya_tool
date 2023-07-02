#coding: uf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from maya import cmds
from maya.common.ui import LayoutManager
import os,functools

#ファイルを開く本処理
def openFile(filePath,*args,**kwargs):
    #拡張子を判別
    type = 'mayaAscii'
    if filePath.split('.')[-1] == 'mb':
        type = 'mayaBinary'
    #ファイルを開く
    cmds.file(filePath,o = True,f = True,type = type)

#Tool 本体
class customFileBrowser():
    #クラスアトリビュートの定義
    def __init__(self,*args,**kwargs):
        #UIの名前
        self.win = 'CustomFileBrouserUI'
        #デフォルトのボタンの色(開いていない、開いた後)
        self.buttonColorList = [[0.2,0.3,0.35],[0.0,0.5,1.0]]
        #ファイルリストを取得する
        self.rootPath = ''
        #ファイルパスのリスト
        self.fileList =[]
        #ファイルを開くボタンコントロールのリストを格納
        self.fileButtonList =[]
        #一度開いたボタンを記憶
        self.opendFileButtonList = []

    #UIをアップデートする
    def updateUi(self,*args,**kwargs):

        #もともと格納されいているボタンの情報を一旦クリアする
        for btn in self.fileButtonList:
            cmds.deleteUI(btn)
        self.fileButtonList[:] =[]
        self.opendFileButtonList[:] =[]

        #ファイルリストを取得
        if not os.path.exists(self.rootPath):
            #rootディレクトリが存在しなかった場合
            self.fileList = []
        else:
            self.fileList = os.listdir(self.rootPath)

        #ボタンを追加する
        indx= 0
        for fileName in self.fileList:
            #Mayaファイルかどうか
            if not fileName.split('.')[-1] in ['ma','mb']:continue

            self.fileButtonList.append(cmds.button(l=fileName,h=20,c=functools.partial(self.openFile,fileName,indx),p=self.btnLayout))
            indx += 1
        #ボタンの色を更新
        self.updateButtonColor()

    #ボタンの色を更新する
    def updateButtonColor(self,*args,**kawargs):
        for btn in self.fileButtonList:
            if btn in self.opendFileButtonList:
                #既に開いた
                cmds.button(btn,e=True,bgc=self.buttonColorList[1])
            else:
                #まだ開いていない
                cmds.button(btn,e=True,bgc=self.buttonColorList[0])
    
    #rootディレクトリパスの設定
    def setPath(self,*args,**kwargs):
        #セットされたrootディレクトリのパスから[\]を[/]に置換して正しく評価されるようにする。
        self.rootPath = args[0].replace('\\',"/")
        #セットされたパスが正しいかどうか
        if not os.path.exists(self.rootPath):
            self.rootPath = ''
        cmds.textField(self.dirPathFiled,e=True,tx=self.rootPath)
        self.updateUi()

    def setPathByDialog(self,*args,**kwargs):
        dirList = cmds.fileDialog2(fm=3,cap= 'Please set root path',okc= 'set')
        if not dirList:return
        self.setPath(dirList[0])
    
    #ファイルを開く前処理(classアトリビュートからファイルパスを生成して、本処理へ渡す)
    def openFile(self,filename,btnIndx,*args,**kwargs):
        #ファイルパスを作成
        filePath = '{}/{}'.format(self.rootPath,filename)
        #ファイルを開く(本処理へ)
        openFile(filePath)
        self.opendFileButtonList.append(self.fileButtonList[btnIndx])

        #ボタンの色を更新
        self.updateButtonColor()

    #指定フォルダ以下のファイル
    def ui(self):
        #もしも既にそのUIがあったら、あらかじめ消しておく
        if cmds.window(self.win,q=True,ex=True):
            cmds.deleteUI(self.win)
        cmds.window(self.win)
        with LayoutManager(cmds.formLayout()) as fl:
            #rootディレクトリを指定するUIを追加
            with LayoutManager(cmds.rowLayout(nc=3,adj=2)) as row:
                cmds.text(l='directory:')
                self.dirPathFiled = cmds.textField(cc= self.setPath)
                cmds.iconTextButton(st= 'iconOnly',image1 = 'browseFolder.png',
                                    c = self.setPathByDialog)
            #ファイルリストを表示するスクロールリストの追加
            self.btnLayout = cmds.scrollLayout(cr = True)
        
        #UI要素の位置調整
        cmds.formLayout(fl,e= True,af= ((row,'top',0),(row,'left',0),(row,'right',0),
                                        (self.btnLayout,'bottom',0),(self.btnLayout,'left',0),
                                        (self.btnLayout,'right',0)),ac=(self.btnLayout,'top',0,row))
        
        cmds.showWindow(self.win)

    def showWindow():
        tool = customFileBrowser()
        tool.ui()
    showWindow()
