# GUI imports
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("AutoInvestBot")
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # changing the background color to black 
        # self.setStyleSheet("background-color: rgb(1%,2%,3%); border: 0px ;") 
        # self.setStyleSheet("QLabel {color: rgb(99%,98%,97%); border: 0px ;}") 
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        # File menu items
        newAct = QAction('New', self)
        
        fileMenu.addAction(newAct)
        
        # Edit menu items
        apiMenu = QMenu('API', self)
        changeKeys = QAction('Change Keys', self)
        apiMenu.addAction(changeKeys)
        
        editMenu.addMenu(apiMenu)
        
        # Initial window settings 
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowTitle('Auto Invest Bot')
        self.show()
        
        label = QLabel("Label")

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)
        
        
class MainMenu(QMenuBar):
  
    def __init__(self, parent=None):
        super().__init__(parent)
        
class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)