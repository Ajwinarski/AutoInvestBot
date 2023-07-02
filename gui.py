# GUI Imports
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

# OS Import
import platform

from modules.csv_handler import CSV_Handler

# Subclass QMainWindow to customise your application's main window


class MainWindow(QMainWindow):
    def __init__(self, csv_handler, *args, **kwargs):
        # super(MainWindow, self).__init__(*args, **kwargs)
        self.csv_handler = csv_handler
        self.symbols: list = self.csv_handler.get_symbols()
        super().__init__()
        # Initial window settings
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowTitle('Auto Invest Bot')
        self.setStyleSheet("background-color: rgb(1%,2%,3%); border: 0px ;")
        self.setStyleSheet("QLabel {color: rgb(99%,98%,97%); border: 0px ;}")
        # Use this once integrated close, minimize, and maximize buttons are available
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Create primary widget
        gui = QWidget()

        # Create application menu
        self.SetupMenu()

        # Create top level layout
        layout = QHBoxLayout()
        layout.setSpacing(10)

        # Add layout views
        layout.addLayout(self.SymbolListLayout(), stretch=1)
        layout.addLayout(self.ContextLayout(), stretch=4)

        gui.setLayout(layout)
        self.setCentralWidget(gui)

    # Layout for symbol list and management
    def SymbolListLayout(self) -> QVBoxLayout:
        # Vertical layout
        symbolListLayout = QVBoxLayout()
        # Label
        label = QLabel('Symbols:')
        # Symbol search layout
        symbolSearchLayout = QHBoxLayout()
        # Text field
        symbolTextField = QLineEdit()
        # Add symbol button
        symbolSearchButton = QPushButton('Add')

        symbolSearchButton.clicked.connect(lambda:
                                           self.AddSymbol(symbolTextField.text()))
        symbolSearchButton.clicked.connect(symbolTextField.clear)

        # Create search layout
        symbolSearchLayout.addWidget(symbolTextField, stretch=4)
        symbolSearchLayout.addWidget(symbolSearchButton, stretch=1)

        # Symbol list
        symbolListWidget = QListWidget()
        symbolListWidget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Maximum)

        # For each symbol in the tickets.csv file, create a list item
        for symbol in self.symbols:
            QListWidgetItem(symbol, symbolListWidget)

        # Vertical layout widget adding
        symbolListLayout.addWidget(label)
        symbolListLayout.addLayout(symbolSearchLayout)
        symbolListLayout.addWidget(symbolListWidget)
        symbolListLayout.setAlignment(Qt.AlignTop)

        return symbolListLayout

    # Layout for symbol tab information
    def ContextLayout(self) -> QVBoxLayout:
        contextLayout = QVBoxLayout()
        contextLayout.addWidget(self.ContextTabView())
        return contextLayout

    # Tab view
    def ContextTabView(self):
        tabs = QTabWidget()
        tabs.addTab(self.OverviewTabUI(), "Overview")
        tabs.addTab(self.ValueTabUI(), "Value")
        return tabs

    # Overview tab view
    def OverviewTabUI(self):
        """Create the Overview page UI."""
        overviewTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Overview Option 1"))
        layout.addWidget(QCheckBox("Overview Option 2"))
        overviewTab.setLayout(layout)
        return overviewTab

    # Value tab view
    def ValueTabUI(self):
        """Create the Value page UI."""
        valueTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Value Option 1"))
        layout.addWidget(QCheckBox("Value Option 2"))
        valueTab.setLayout(layout)
        return valueTab

    # Application menu view
    def SetupMenu(self):
        # Check OS to account for MacOS users
        if platform.uname().system.startswith('Darw'):
            # parentless menu bar for MacOS
            self._menu_bar = QMenuBar()
        else:
            # refer to the default one
            self._menu_bar = self.menuBar()

        # Menu items
        self.file_menu = self._menu_bar.addMenu('&File')
        self.edit_menu = self._menu_bar.addMenu('&Edit')
        self.view_menu = self._menu_bar.addMenu('&View')
        self.accounts_menu = self._menu_bar.addMenu('&Accounts')
        self.help_menu = self._menu_bar.addMenu('&Help')

        # File menu items
        newAct = QAction('New', self)
        self.file_menu.addAction(newAct)

        # Edit menu items
        apiMenu = QMenu('API', self)
        changeKeys = QAction('Change Keys', self)
        apiMenu.addAction(changeKeys)
        self.edit_menu.addMenu(apiMenu)

    def AddSymbol(self, text: str):
        self.csv_handler.get_stock_data(text)
        pass

# class MainMenu(QMenuBar):

#     def __init__(self, parent=None):
#         super().__init__(parent)


# class MyPopup(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)

#     def paintEvent(self, e):
#         dc = QPainter(self)
#         dc.drawLine(0, 0, 100, 100)
#         dc.drawLine(100, 0, 0, 100)
