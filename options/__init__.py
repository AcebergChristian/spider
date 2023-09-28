import json
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import options.data as static


class Options(QWidget):

    #options 发出去的信号 给gather采集规则
    tomsg = Signal(dict)
    
    def __init__(self):
        super().__init__()

        self.create_options_group()

    def create_options_group(self):

        # 获取默认键值对数据
        self.optionlist = static.data["optionlist"]

        # 右侧设置栏
        self.options_group = QFrame()
        self.options_group.hide()
        self.options_group.setFixedWidth(200)
        self.options_group.setStyleSheet(
            "background-color:{}".format(static.data["options"]["bg"]))
        self.options_group_QV = QVBoxLayout()
        self.options_group_QV.setSpacing(20)
        # 装list的QV 外面套一个滚动布局
        self.options_list_QV = QVBoxLayout()

        self.options_group.setLayout(self.options_group_QV)

        self.createlistbtn()
        self.createlisttitle()
        self.createlistitemQV()
        self.createlistitem()

    def createlistbtn(self):
        option_list_btb_QH = QHBoxLayout()
        # 新增按钮
        option_list_addbtn = Buttonclass("+添加")
        option_additem = self.option_additem_decorator()
        option_list_addbtn.clicked.connect(option_additem)
        option_list_btb_QH.addWidget(option_list_addbtn)

        # 清空按钮
        option_list_clearbtn = Buttonclass("清空")
        option_clearitem = self.option_clearitem_decorator()
        option_list_clearbtn.clicked.connect(option_clearitem)
        option_list_btb_QH.addWidget(option_list_clearbtn)
        
        # 清空按钮
        option_list_savebtn = Buttonclass("保存")
        option_saveitem = self.option_saveitem_decorator()
        option_list_savebtn.clicked.connect(option_saveitem)
        option_list_btb_QH.addWidget(option_list_savebtn)


        self.options_group_QV.addLayout(option_list_btb_QH)
        

    def createlisttitle(self):

        option_title_QH = QHBoxLayout()
        option_title_QH.setAlignment(Qt.AlignHCenter)
        option_title_QH.setSpacing(60)
        option_title_QH_filed = QLabel("Filed")
        option_title_QH_path = QLabel("XPath")
        option_title_QH.addWidget(option_title_QH_filed)
        option_title_QH.addWidget(option_title_QH_path)
        self.options_group_QV.addLayout(option_title_QH)


    def createlistitemQV(self):
        self.options_group_QV.addLayout(self.options_list_QV)
        self.options_group_QV.addStretch()

    def createlistitem(self):
        
        while self.options_list_QV.count():
                item = self.options_list_QV.takeAt(0)
                while item.count():
                    hitem = item.takeAt(0)
                    if hitem.widget():
                        hitem.widget().setParent(None)
                        hitem.widget().deleteLater()
                # 从原始布局中移除 QHBoxLayout
                self.options_list_QV.removeItem(item)
                item.setParent(None)
                item.deleteLater()

        for index, item in enumerate(self.optionlist):
            option_list_QH = QHBoxLayout()
            option_list_QH_filed = QLineEdit()
            option_list_QH_filed.editingFinished.connect(self.option_update_optionlist)
            option_list_QH_filed.setPlaceholderText(item[0]["option_filed"])
            option_list_QH_filed.setText(item[0]["option_filed_val"])
            option_list_QH_filed.setFixedSize(80, 26)
            option_list_QH_filed.setStyleSheet(
                "background:rgb(229,230,235);color:#333333")
            option_list_QH_path = QLineEdit()
            option_list_QH_path.editingFinished.connect(self.option_update_optionlist)
            option_list_QH_path.setPlaceholderText(item[1]["option_path"])
            option_list_QH_path.setText(item[1]["option_path_val"])
            option_list_QH_path.setFixedSize(80, 26)
            option_list_QH_path.setStyleSheet(
                "background:rgb(229,230,235);color:#333333")

            option_list_QH.addWidget(option_list_QH_filed)
            option_list_QH.addWidget(option_list_QH_path)

            self.options_list_QV.addLayout(option_list_QH)


    # 新增filed和path槽函数
    def option_additem_decorator(self):
        def option_additem_func():
            #把所有Qlinedit 焦点全部失焦一遍，用于触发保存每个的值给self.optionlist
            for itemQH in self.options_list_QV.children():
                itemQH.itemAt(0).widget().clearFocus()
                itemQH.itemAt(1).widget().clearFocus()
                
            itemdata = [{"option_filed": "filed","option_filed_val":""}, {"option_path": "path","option_path_val":"" }]
            self.optionlist.append(itemdata)
            self.createlistitem()
        return option_additem_func


    # 清空filed和path槽函数
    def option_clearitem_decorator(self):
        def option_clearitem_func():
            self.optionlist = []
            while self.options_list_QV.count():
                item = self.options_list_QV.takeAt(0)
                while item.count():
                    hitem = item.takeAt(0)
                    if hitem.widget():
                        hitem.widget().setParent(None)
                        hitem.widget().deleteLater()
                # 从原始布局中移除 QHBoxLayout
                self.options_list_QV.removeItem(item)
                item.setParent(None)
                item.deleteLater()
        
        return option_clearitem_func

    #点击保存触发 获取用户输入的值并形成数组  给爬虫
    def option_saveitem_decorator(self):
        def option_saveitem_func():
            res = []
            for itemQH in self.options_list_QV.children():
                res.append({"filed":itemQH.itemAt(0).widget().text(),"xpath":itemQH.itemAt(1).widget().text()})
            
            self.create_data_json("static/options.json",res)
            
            self.save_shownoticedialog()
        return option_saveitem_func
    
    #Qliineedit失焦时候触发 获取用户输入的值更新 self.optionlist
    def option_update_optionlist(self):
            #获取用户输入的值
            get_optionlist_val=[]
            for itemQH in self.options_list_QV.children():
                get_optionlist_val.append({"filed":itemQH.itemAt(0).widget().text(),"xpath":itemQH.itemAt(1).widget().text()})
            # #更新 self.optionlist
            for index,item in enumerate(get_optionlist_val):
                self.optionlist[index][0]["option_filed_val"] = item["filed"]
                self.optionlist[index][1]["option_path_val"] = item["xpath"]
            # print(self.optionlist)
       
    def save_shownoticedialog(self):
        self.noticeDialog = NoticeDialog("保存成功")
        self.noticeDialog.show()
    

    ######信号连接######
    #接受menu发出的信号方法
    @Slot(str)
    def getmenu_toggleoptions(self, msg):
        self.options_group.setHidden(msg["toggle_option"])
        self.options_group.update
 
    ######信号连接######
    
    #创建本地 json文件方法，用于存储options传来的json数据
    def create_data_json(self,filename,args):
        with open(filename, 'w') as f:
            json.dump(args,f)


# 按钮样式的类
class Buttonclass(QPushButton):
    def __init__(self, arg):
        super().__init__()

        self.setText(arg)
        self.setFixedSize(52, 26)
        self.setStyleSheet(
            "background-color:rgb(86,100,154);color:#ffffff;border-radius:2px;")

    def enterEvent(self, event):
        self.setStyleSheet(
            "background-color:rgba(86,100,154,0.8);color:#ffffff;border-radius:2px;")

    def leaveEvent(self, event):
        self.setStyleSheet(
            "background-color:rgba(86,100,154,1);color:#ffffff;border-radius:2px;")
        

class NoticeDialog(QDialog):
    def __init__(self,arg,parent=None):
        super().__init__(parent)
        self.setWindowTitle("提示")
        self.setWindowModality(Qt.ApplicationModal)
        
        self.arg = arg
        
        self.setFixedSize(200,120)
        self.label= QLabel(self.arg)
        self.confirm= QPushButton("确定")
        self.confirm.clicked.connect(self.close_noticeDialog)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.confirm)

        self.setLayout(layout)
        
    def close_noticeDialog(self):
        self.close()