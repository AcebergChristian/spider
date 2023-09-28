from os import stat
import random
import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import menu.data as static
 
class Menu(QWidget):
    
    #Menu 发出去的信号 显隐 options
    tomsg = Signal(dict)
        
        
    def __init__(self):
        super().__init__()
        
        self.create_menu_group()

    def create_menu_group(self):
        #左侧菜单栏
        self.menu_group = QFrame()
        self.menu_group.setFixedWidth(80)
        self.menu_group.setStyleSheet("background-color:{}".format(static.data["menu"]["bg"]))
        
        self.menu_QV = QVBoxLayout()
        self.menu_QV.setContentsMargins(0,20,0,0)
        
        self.createmenu()
        
        self.menu_group.setLayout(self.menu_QV)
        
    def createmenu(self):
        menulist = static.data["menulist"]
        
        #垂直布局装logo
        menulist_logo_QH = QHBoxLayout()
        menulist_logo = QLabel()
        menulist_logo.setFixedSize(60,60)
        pixmap_logo = QPixmap(menulist[0]["path"])
        scaled_pixmap = pixmap_logo.scaled(menulist_logo.size())
        menulist_logo.setPixmap(scaled_pixmap)
        
        menulist_logo_QH.addWidget(menulist_logo)
        
        self.menu_QV.addLayout(menulist_logo_QH)
        #self.menu_QV.addStretch()
        
        #垂直布局装list
        menulist_QV = QVBoxLayout()
        menulist_QV.setContentsMargins(0,30,0,0)
        
        for index,item in enumerate(menulist):
            if index > 0 and index < 2:
                menuitem_frame = Menuframe()
                menuitem_frame.setFixedSize(80,64)
                menuitem_frame.setStyleSheet("background:rgba(255,255,255,0);border-radius:0px;")
                
                menuitem_frame_QV = QVBoxLayout()
                #menuitem_frame_QV.setContentsMargins(0,0,0,0)
                menuitem_frame_QV.setSpacing(4)
                
                menuitem_frame_QV_icon = QFrame()
                menuitem_frame_QV_icon.setFixedSize(60,20)
                menuitem_frame_QV_icon.setStyleSheet("background:url({}) no-repeat center center;".format(item["path"]))
                
                menuitem_frame_QV_text = QLabel(item["text"])
                menuitem_frame_QV_text.setStyleSheet("color:#ffffff")
                menuitem_frame_QV_text.setAlignment(Qt.AlignHCenter)
                menuitem_frame_QV_text.setFixedSize(60,14)
                
                menuitem_frame_QV.addWidget(menuitem_frame_QV_icon)
                menuitem_frame_QV.addWidget(menuitem_frame_QV_text)
                menuitem_frame_QV.setSpacing(0)
            
                menuitem_frame.setLayout(menuitem_frame_QV)
            
                menulist_QV.addWidget(menuitem_frame)
                
                
        self.menu_QV.addLayout(menulist_QV)
        self.menu_QV.addStretch()
        
        #垂直布局装设置
        self.option_flag = True
        menuitem_frame = Menuframe()
        menuitem_frame.mousePressEvent = lambda event: self.toggle_option(event)

        menuitem_frame.setFixedSize(80,64)
        menuitem_frame.setStyleSheet("background:rgba(255,255,255,0);border-radius:0px;")
        
        menuitem_frame_QV = QVBoxLayout()
        #menuitem_frame_QV.setContentsMargins(0,0,0,0)
        menuitem_frame_QV.setSpacing(4)
        
        menuitem_frame_QV_icon = QFrame()
        menuitem_frame_QV_icon.setFixedSize(60,20)
        menuitem_frame_QV_icon.setStyleSheet("background:url({}) no-repeat center center;".format(menulist[2]["path"]))
        
        menuitem_frame_QV_text = QLabel(menulist[2]["text"])
        menuitem_frame_QV_text.setStyleSheet("color:#ffffff")
        menuitem_frame_QV_text.setAlignment(Qt.AlignHCenter)
        menuitem_frame_QV_text.setFixedSize(60,14)
        
        menuitem_frame_QV.addWidget(menuitem_frame_QV_icon)
        menuitem_frame_QV.addWidget(menuitem_frame_QV_text)
        menuitem_frame_QV.setSpacing(0)
    
        menuitem_frame.setLayout(menuitem_frame_QV)
        
        self.menu_QV.addWidget(menuitem_frame)
        
        #垂直布局装my
        menulist_my_QH = QHBoxLayout()
        menulist_my = QFrame()
        menulist_my.setFixedSize(60,60)
        menulist_my.setStyleSheet("background:url({}) no-repeat center center;border-radius:20px;".format(menulist[3]["path"]))
        menulist_my_QH.addWidget(menulist_my)
        
        self.menu_QV.addLayout(menulist_my_QH)
    
    ######信号连接######
    #点击判断显隐，并发送信号
    def toggle_option(self, event):
        self.option_flag = False if self.option_flag else True
        self.toggle_option_signal({"toggle_option":self.option_flag})
        
    #发送显示隐藏option的信号
    def toggle_option_signal(self,arg):
        self.tomsg.emit(arg)

        
        
#重写menu的 QFrame 实现样式和事件       
class Menuframe(QFrame):

    def __init__(self):
        super().__init__()
        self.flag = False
        self.setStyleSheet("background-color:rgba(54,64,95,0);")
                                                        
    def enterEvent(self, event):
        self.setStyleSheet("background-color:rgba(62,101,224,1);border-radius:0px;")

    def leaveEvent(self, event):
        if self.flag != True:
            self.setStyleSheet("background-color:rgba(106,181,252,0)")