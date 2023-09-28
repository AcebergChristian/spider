import sys
from PySide6 import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #图标
    app.setWindowIcon(QIcon('./static/logo.png'))
    
    window = MainWindow()

    window.resize(1060,680)
    window.show()
    
    
    sys.exit(app.exec())