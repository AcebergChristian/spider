from PySide6.QtWidgets import *
from PySide6 import *
from PySide6.QtCore import *
import mainwindow.data as static
from menu import Menu
from nav import Nav
from options import Options
from gather import Gather
from gather import Ace_spider
 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        
        self.setWindowTitle(static.data["mainwindow"]["TITLE"])
        self.setMinimumSize(800,640)
        #样式
        self.setStyleSheet("background:{};border-radius:10px;".format(static.data["mainwindow"]["bg"]))
        #无边框
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        #初始化组件 布局
        self.createlayout()
        
        #连接menu_options_toggle的信号
        self.connect_menu_toggleoption_signal()

        

    def createlayout(self):
        #纵向布局,包括 nav 和 body
        self.main_QV = QVBoxLayout()
        self.main_QV.setContentsMargins(0,0,0,0)
        self.main_QV.setSpacing(0)
        
        #横向布局,body的
        self.main_QH = QHBoxLayout()
        self.main_QH.setContentsMargins(5,5,5,5)
        self.main_QH.setSpacing(10)
        
        #导入nav
        self.nav = Nav()
        #导入menu
        self.menu = Menu()
        #导入gather
        self.gather = Gather()
        #导入gather里的Ace_spider
        self.acespider = Ace_spider()
        #导入options
        self.options = Options()
        
        #横向布局添加menu
        self.main_QH.addWidget(self.menu.menu_group)
        self.main_QH.addLayout(self.gather.main_QH)
        self.main_QH.addWidget(self.options.options_group )
        
        
        #主界面纵向布局添加组件
        self.main_QV.addWidget(self.nav.topnav_group)
        self.main_QV.addLayout(self.main_QH)
        
        self.setLayout(self.main_QV)
        
        
    ######信号连接######
    #执行leftmenu的信号方法显隐 option板块
    def connect_menu_toggleoption_signal(self):
        self.menu.tomsg.connect(self.options.getmenu_toggleoptions)