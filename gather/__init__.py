from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
import math
from lxml import etree
import requests
import pandas as pd
import threading
import gather.data as static


#UI类
class Gather(QWidget):
    
    
    def __init__(self):
        super().__init__()


        self.create_gather_group()
        
        self.main_QH = QHBoxLayout()
        self.main_QH.addLayout(self.create_gather_group())
        
        
        # 获取Ace_spider 实例化对象
        self.spider = Ace_spider()
 
        # 创建 LoadingDialog 实例
        self.loading_dialog = LoadingDialog()
        
        # 获取 SaveFile_Dialog实例化对象
        self.savefile_dialog = SaveFile_Dialog()
        
        # 获取参数不正确时候的dialog
        self.show_error = NoticeDialog("参数不正确,请检查")

    def create_gather_group(self):
        
        # 主体
        gather_frame_QV = QVBoxLayout()
        
        #参数栏倒入垂直布局第一行 参数栏
        gather_frame_QV.addWidget(self.create_gather_argQH_group())
        #参数栏倒入垂直布局第一行 表格栏
        gather_frame_QV.addWidget(self.create_gather_tablebtn())
        #参数栏倒入垂直布局第一行 表格栏
        gather_frame_QV.addWidget(self.create_gather_table())
        gather_frame_QV.addStretch()
        
        #返回垂直布局设置为总布局
        return gather_frame_QV
        
    
    def create_gather_argQH_group(self):
        gather_frame_QV_argsQH_group = QGroupBox()
        gather_frame_QV_argsQH_group.setStyleSheet("background:{}".format(static.data["gather"]["bg"]))
        gather_frame_QV_argsQH = QHBoxLayout()
        
        #输入链接组件
        self.gather_frame_QV_argsQH_urlform = QFormLayout()
        self.gather_frame_QV_argsQH_urlformurl = QLabel("Url")
        self.gather_frame_QV_argsQH_urlformurl.setStyleSheet("color:#333333")
        self.gather_frame_QV_argsQH_urlformlabel = QLineEdit()
        self.gather_frame_QV_argsQH_urlformlabel.setFixedSize(160, 26)
        self.gather_frame_QV_argsQH_urlformlabel.setStyleSheet("background:rgb(229,230,235);color:#333333")
        self.gather_frame_QV_argsQH_urlform.addRow(self.gather_frame_QV_argsQH_urlformurl,self.gather_frame_QV_argsQH_urlformlabel)
        gather_frame_QV_argsQH.addLayout(self.gather_frame_QV_argsQH_urlform)
        
        #输入从第几页开始
        self.gather_frame_QV_argsQH_pageform = QFormLayout()
        self.gather_frame_QV_argsQH_urlformfrom = QLabel("From")
        self.gather_frame_QV_argsQH_urlformfrom.setStyleSheet("color:#333333")
        self.gather_frame_QV_argsQH_pageformlabel = QLineEdit()
        self.gather_frame_QV_argsQH_pageformlabel.setFixedSize(50, 26)
        self.gather_frame_QV_argsQH_pageformlabel.setStyleSheet("background:rgb(229,230,235);color:#333333")
        self.gather_frame_QV_argsQH_pageform.addRow(self.gather_frame_QV_argsQH_urlformfrom, self.gather_frame_QV_argsQH_pageformlabel)
        gather_frame_QV_argsQH.addLayout(self.gather_frame_QV_argsQH_pageform)
        
        #输入爬到第几页数
        self.gather_frame_QV_argsQH_pageto = QFormLayout()
        self.gather_frame_QV_argsQH_urlformto = QLabel("To")
        self.gather_frame_QV_argsQH_urlformto.setStyleSheet("color:#333333")
        self.gather_frame_QV_argsQH_pagetolabel = QLineEdit()
        self.gather_frame_QV_argsQH_pagetolabel.setFixedSize(50, 26)
        self.gather_frame_QV_argsQH_pagetolabel.setStyleSheet("background:rgb(229,230,235);color:#333333")
        self.gather_frame_QV_argsQH_pageto.addRow(self.gather_frame_QV_argsQH_urlformto, self.gather_frame_QV_argsQH_pagetolabel)
        gather_frame_QV_argsQH.addLayout(self.gather_frame_QV_argsQH_pageto)
        
        #输入数组的外层的xpath
        self.gather_frame_QV_argsQH_clickform = QFormLayout()
        self.gather_frame_QV_argsQH_urlformto = QLabel("Par_xpath")
        self.gather_frame_QV_argsQH_urlformto.setStyleSheet("color:#333333")
        self.gather_frame_QV_argsQH_clickformlabel = QLineEdit()
        self.gather_frame_QV_argsQH_clickformlabel.setFixedSize(150, 26)
        self.gather_frame_QV_argsQH_clickformlabel.setStyleSheet("background:rgb(229,230,235);color:#333333")
        self.gather_frame_QV_argsQH_clickform.addRow(self.gather_frame_QV_argsQH_urlformto, self.gather_frame_QV_argsQH_clickformlabel)
        gather_frame_QV_argsQH.addLayout(self.gather_frame_QV_argsQH_clickform)
        
        gather_frame_QV_argsQH.addStretch()
        
        #清空和采集btn
        gather_frame_QV_argsQH_clearbtn = Buttonclass("清空")
        gather_frame_QV_argsQH_clearbtn.clicked.connect(self.cleargather_arg)
        gather_frame_QV_argsQH_gatherbtn = Buttonclass("采集")
        gather_frame_QV_argsQH_gatherbtn.clicked.connect(self.getgather_arg)
        gather_frame_QV_argsQH.addWidget(gather_frame_QV_argsQH_clearbtn)
        gather_frame_QV_argsQH.addWidget(gather_frame_QV_argsQH_gatherbtn)
        
        gather_frame_QV_argsQH.addStretch()
        
        gather_frame_QV_argsQH_group.setLayout(gather_frame_QV_argsQH)
        
        return gather_frame_QV_argsQH_group
    
    def create_gather_tablebtn(self):
        gather_frame_QV_tablebtnQH_group = QGroupBox()
        gather_frame_QV_tablebtnQH_group.setStyleSheet("background:rgb(255,255,255)")
        gather_frame_QV_tablebtnQH = QHBoxLayout()
        
        #导出按钮
        gather_frame_QV_argsQH_outputbtn = Buttonclass("导出")
        gather_frame_QV_argsQH_outputbtn.clicked.connect(self.click_export)
        
        gather_frame_QV_tablebtnQH.addWidget(gather_frame_QV_argsQH_outputbtn)
        
        gather_frame_QV_tablebtnQH.addStretch()
        
        gather_frame_QV_tablebtnQH_group.setLayout(gather_frame_QV_tablebtnQH)
        
        return gather_frame_QV_tablebtnQH_group
    
    def create_gather_table(self):
        tablewid = Tablewid()
        return tablewid.gather_frame_QV_table_group

    #点击导出btn 打开dialog
    def click_export(self):
        self.savefile_dialog.show()
        self.savefile_dialog.getspider_data(self.spider.outdata)

    #点击采集获取用户输入的数据
    def getgather_arg(self):
        url = self.gather_frame_QV_argsQH_urlformlabel.text()
        frompage = self.gather_frame_QV_argsQH_pageformlabel.text()
        topage = self.gather_frame_QV_argsQH_pagetolabel.text()
        clickpath = self.gather_frame_QV_argsQH_clickformlabel.text()
        self.gather_args = [url,frompage,topage,clickpath]
        
        self.getoptions_json = self.get_data_json("static/options.json")
        
        self.spider = Ace_spider()
        self.spider_thread = threading.Thread(target=self.spider.start_spider, args=(self.gather_args,self.getoptions_json))
        
        # 创建 LoadingDialog 实例
        self.loading_dialog = LoadingDialog()

        # 将信号连接到对话框的槽函数
        self.spider.tomsg_progress_dialog.connect(self.loading_dialog.set_progress)

        if url and frompage and topage and clickpath:
            
            # 在爬虫线程启动之前显示对话框
            self.loading_dialog.show()
            
            # 启动爬虫线程
            self.spider_thread.start()
        
        else:
            self.show_error.show()
        
        
    def cleargather_arg(self):
        self.gather_frame_QV_argsQH_urlformlabel.setText("")
        self.gather_frame_QV_argsQH_pageformlabel.setText("")
        self.gather_frame_QV_argsQH_pagetolabel.setText("")
        self.gather_frame_QV_argsQH_clickformlabel.setText("")
    
    def get_data_json(self,filename):
        with open(filename, 'r') as f:
            return json.load(f)
        
        
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

class Tablewid(QWidget):
    instances = []

        
    def __init__(self):
        super().__init__()
        
        self.instances.append(self)
        
        self.getcolumnData = static.data["gather"]["rawdata"]["columndata"]
        self.getData = static.data["gather"]["rawdata"]["fakedata"]
        #从获取爬虫的数据
        self.Ace_getcolumnData = static.data["gather"]["rawdata"]["columndata"]
        self.Ace_getData = static.data["gather"]["rawdata"]["fakedata"]
        
        self.gather_frame_QV_table_group = QGroupBox("")
        self.gather_frame_QV_table_group.setStyleSheet("background:rgb(255,255,255)")
        self.gather_frame_QV_table_groupQV = QVBoxLayout()
        
        #记录当前页数
        self.currentpage = 1
        #self.get_gotobtntext = 1
        self.createtable(self.getData,self.getcolumnData)
        self.createtablepagebar()
        
        self.gather_frame_QV_table_group.setLayout(self.gather_frame_QV_table_groupQV)


    # 创建表格
    def createtable(self,arg1,arg2):
        #默认表格
        self.tableWidget = QTableWidget(10, 8)
        self.tableWidget.setFixedHeight(300)
        self.tableWidget.setHorizontalHeaderLabels(arg2)
        
        self.tableWidget.setStyleSheet(
            "QTableWidget::item { color:#333333;font-size:8px;border:0px solid rgb(255,255,11)}  QTableView::item:selected { background-color: rgba(81,93,128,0.3);  }")
        self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { color:#333333;font-weight:500;font-size:12px; }")
        self.tableWidget.verticalHeader().setStyleSheet(
            "QHeaderView::section { color:#333333;font-weight:500;font-size:12px; }")
        self.tableWidget.horizontalScrollBar().setStyleSheet(
            "QScrollBar:horizontal { background: rgb(208,209,210); height: 12px;  }")
        self.tableWidget.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical {  background: rgb(208,209,210); width: 12px;  }")
        
        #默认表格的数据
        for index, item in enumerate(arg1):
            for yndex,itemfiled in enumerate(arg2):
                self.tableWidget.setItem(index, yndex, QTableWidgetItem(item[itemfiled]))
                
        self.gather_frame_QV_table_groupQV.addWidget(self.tableWidget)
        
    #只更新self.Ace_getcolumnData、self.Ace_getcolumnData,不更新表格,用于获取新爬虫数据
    def updatedata(self,arg1,arg2):
        self.Ace_getcolumnData = arg2
        self.Ace_getData = arg1
        
        self.updatetabledata(self.Ace_getData,self.Ace_getcolumnData)
        
    #更新表格和数据,用于翻页时
    def updatetabledata(self,arg1,arg2):

        #清理表格数据 重新生成列和行
        self.tableWidget.clear()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(len(arg2)+2)
        
        #更新表格表头
        self.tableWidget.setHorizontalHeaderLabels(arg2)
        
        #更新表格数据
        for row, item in enumerate(arg1):  # 使用enumerate创建新的行索引
            for col, itemfield in enumerate(arg2):
                self.tableWidget.setItem(row, col, QTableWidgetItem(item[itemfield]))
        
        # print(self.Ace_getcolumnData)


    # 生成点击页数槽函数
    def btnclickfunc_decorator(self, flag):
        if flag == "next":
            def btnclickfunc():
                self.currentpage = self.currentpage+1 if self.currentpage<math.ceil(len(self.Ace_getData) / 10) else math.ceil(len(self.Ace_getData) / 10) 
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(self.currentpage),self.Ace_getcolumnData)
        elif flag == "pre":
            print(self.currentpage)
            def btnclickfunc():
                self.currentpage = self.currentpage-1 if self.currentpage>1 else 1
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(self.currentpage),self.Ace_getcolumnData)
        elif flag == "fir":
            def btnclickfunc():
                self.currentpage = 1
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(1),self.Ace_getcolumnData)
        elif flag == "lst":
            def btnclickfunc():
                self.currentpage = math.ceil(len(self.Ace_getData) / 10)
                self.gather_frame_QV_tablewid_pagebarformlabel.setText(str(self.currentpage))
                self.updatetabledata(self.somepagedata(self.currentpage),self.Ace_getcolumnData)
        elif flag == "goto":
            def btnclickfunc():
                gotopage = self.gather_frame_QV_tablewid_pagebarformlabel.text()
                gotopage = int(gotopage) if gotopage != "" else 1
                self.currentpage = gotopage
                self.updatetabledata(self.somepagedata(gotopage),self.Ace_getcolumnData)
        else:
            def btnclickfunc():
                self.updatetabledata(self.somepagedata(self.currentpage),self.Ace_getcolumnData)
        return btnclickfunc

    # 生成失焦获取 edit的文字槽函数
    def blurgettext(self):
        get_gotobtntext = self.gather_frame_QV_tablewid_pagebarformlabel.text()
        print("Text changed:", get_gotobtntext)
    

    def createtablepagebar(self):
        pagebar_QH = QHBoxLayout()

        firstpbtn = Buttonclass("首页")
        btnclick_funcnfir = self.btnclickfunc_decorator("fir")
        firstpbtn.clicked.connect(btnclick_funcnfir)
        
        lastpbtn = Buttonclass("尾页")
        btnclick_funcnlst = self.btnclickfunc_decorator("lst")
        lastpbtn.clicked.connect(btnclick_funcnlst)
        
        prebtn = Buttonclass("<")
        btnclick_funcnpre = self.btnclickfunc_decorator("pre")
        prebtn.clicked.connect(btnclick_funcnpre)
        
        nextbtn = Buttonclass(">")
        btnclick_funcnnext = self.btnclickfunc_decorator("next")
        nextbtn.clicked.connect(btnclick_funcnnext)
        
        #跳转页 input
        self.gather_frame_QV_tablewid_pagebarformlabel = QLineEdit()
        self.gather_frame_QV_tablewid_pagebarformlabel.setFixedSize(40, 26)
        self.gather_frame_QV_tablewid_pagebarformlabel.setStyleSheet("background:rgb(229,230,235);color:#333333")
        gotobtn = Buttonclass("跳转")
        btnclick_funcngoto = self.btnclickfunc_decorator("goto")
        gotobtn.clicked.connect(btnclick_funcngoto)

        pagebar_QH.addStretch()
        pagebar_QH.addWidget(firstpbtn)
        pagebar_QH.addWidget(prebtn)
        pagebar_QH.addWidget(self.gather_frame_QV_tablewid_pagebarformlabel)
        pagebar_QH.addWidget(gotobtn)
        pagebar_QH.addWidget(nextbtn)
        pagebar_QH.addWidget(lastpbtn)
        
        self.gather_frame_QV_table_groupQV.addLayout(pagebar_QH)
    

    # 根据点击的数字，展示某一页数据
    def somepagedata(self, arg):
        res = []
        for index, item in enumerate(self.Ace_getData):
            if 10*arg-10 < index <= 10*arg:
                res.append(item)
        #print(res)
        return res
    
    
# dialog 采集爬虫时的 dialog
class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("爬虫")
        self.setWindowModality(Qt.ApplicationModal)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.label= QLabel()
        
        self.btn_layout = QHBoxLayout()
        self.confirm= QPushButton("确定")
        self.confirm.clicked.connect(self.close_loadingDialog)
        self.cancel= QPushButton("取消")
        self.cancel.clicked.connect(self.close_loadingDialog)
        
        self.btn_layout.addWidget(self.confirm)
        self.btn_layout.addWidget(self.cancel)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.btn_layout)

        self.setLayout(self.layout)
        
    def set_progress(self, value):
        self.label.setText(f"{round(value,1)}%")
        self.progress_bar.setValue(value)
        
    def close_loadingDialog(self):
        self.close()
        
    
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
    
    
#爬虫类        
class Ace_spider(QObject):
    
    tomsg_progress_dialog = Signal(int)  # 定义用于更新进度条的信号
    
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        #获取获取表格的实例化对象
        self.table_instance = Tablewid.instances[1]
        
        #装爬虫数据的对象
        self.outdata = {"columndata":[],"tabledata":[]}
        
    #创建本地 json文件方法，用于存储options传来的json数据
    def create_data_json(self,filename,args):
        with open(filename, 'w') as f:
            json.dump(args,f)
    
    #从 .json文件 获取数据json
    def get_data_json(self,filename):
        with open(filename, 'r') as f:
            return json.load(f)
    
    # 开始爬虫方法， 点击采集btn时候，在接受信号的方法getgather_args 里面触发
    def start_spider(self, gather_args, options_args):
    
        outdata_columndata = []
        for item in options_args:
            outdata_columndata.append(item["filed"])
        self.outdata["columndata"] = outdata_columndata
        
        self.outdata_tabledata = []
        
        crawler_thread = threading.Thread(target=self.crawl, args=(gather_args, options_args))
        crawler_thread.start()

    
    def crawl(self, gather_args, options_args):
        total_iterations = int(gather_args[2]) - int(gather_args[1]) + 1
        
        for i in range(int(gather_args[1]), int(gather_args[2]) + 1):
            response = requests.get(
                gather_args[0].format(str(i)),
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                    "Connection": "close"
                },
                stream=True,
                timeout=50
            )
            data = etree.HTML(response.content)
            
            allli = data.xpath(gather_args[3])
            for lst in allli:
                outdata_tabledata_item = {}
                for item in options_args:
                    outdata_tabledata_item[item["filed"]] = lst.xpath(item["xpath"])[0] if lst.xpath(item["xpath"]) else "无"
                
                self.outdata_tabledata.append(outdata_tabledata_item)
            
            response.close()
            
            progress = (i - int(gather_args[1]) + 1) / total_iterations * 100
            # 发送信号更新进度条
            self.tomsg_progress_dialog.emit(progress)
            
            QThread.msleep(500)
        
        self.outdata["tabledata"] = self.outdata_tabledata
        self.table_instance.updatedata(self.outdata["tabledata"], self.outdata["columndata"])
        

        

class SaveFile_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #初始化数据
        self.save_data={}
        
        self.setWindowTitle("导出文件")
        self.setWindowModality(Qt.ApplicationModal)

        layoutQV = QVBoxLayout()
        layoutQH = QHBoxLayout()
        
        #获取保存路径
        self.showsavefile_path = QLineEdit()
        self.showsavefile_path.setReadOnly(True)
        self.showsavefile_path.setFixedSize(240, 26)
        self.showsavefile_path.setStyleSheet("color:#333333")
        
        #获取保存路径
        #self.getsavefile_path=""
        self.savefile_btn = Buttonclass("选择")
        self.savefile_btn.clicked.connect(self.select_path)
        
        #下拉选择导出文件类型 csv、xsml、xml、txt、json
        self.combo_selecttype = QComboBox()
        self.combo_selecttype.currentIndexChanged.connect(self.select_type)
        self.combo_selecttype.addItem("csv")
        self.combo_selecttype.addItem("xlsx")
        self.combo_selecttype.addItem("txt")
        self.combo_selecttype.addItem("json")

        # 设置默认选中项
        self.combo_selecttype.setCurrentIndex(0)
        
        
        #确认导出并关闭dialog
        savefile_savebtn = Buttonclass("确认")
        savefile_savebtn.clicked.connect(self.confirm_close_dialog)
        
        layoutQH.addWidget(self.showsavefile_path)
        layoutQH.addWidget(self.savefile_btn)
        
        layoutQV.addLayout(layoutQH)
        layoutQV.addWidget(self.combo_selecttype)
        layoutQV.addWidget(savefile_savebtn)
        
        
        self.setLayout(layoutQV)
        
    #获取数据方法
    def getspider_data(self,arg):
        self.save_data = arg
        
    
    #选择保存路径
    def select_path(self):
        # 打开文件对话框
        self.getsavefile_path = QFileDialog.getExistingDirectory(None, "选择路径", "", QFileDialog.ShowDirsOnly)
        self.showsavefile_path.setText(self.getsavefile_path)

    #选择保存文件类型
    def select_type(self):
        self.selected_item = self.combo_selecttype.currentIndex()
        print(f"选择了：{self.combo_selecttype.currentText()}")
        
    def confirm_close_dialog(self):

        if self.showsavefile_path.text():
            if self.selected_item == 0: #csv
                with open(self.getsavefile_path+"/spiderdata.csv", 'w') as f:
                    df = pd.DataFrame(self.save_data["tabledata"], columns=self.save_data["columndata"])
                    df.to_csv(self.getsavefile_path+"/spiderdata.csv", index=False)
            elif self.selected_item == 1: #xlsx
                with open(self.getsavefile_path+"/spiderdata.xlsx", 'w') as f:
                    df = pd.DataFrame(self.save_data["tabledata"], columns=self.save_data["columndata"])
                    df.to_excel(self.getsavefile_path+"/spiderdata.xlsx", index=False)
            elif self.selected_item == 2: #txt
                with open(self.getsavefile_path+"/spiderdata.txt", 'w') as f:
                    json.dump(self.save_data,f,ensure_ascii=False,indent=2)
            elif self.selected_item == 3: #json
                with open(self.getsavefile_path+"/spiderdata.json", 'w') as f:
                    json.dump(self.save_data,f,ensure_ascii=False,indent=2)
            self.close()
        else:
            self.shownotice = NoticeDialog("请输入完整参数")
            self.shownotice.show()