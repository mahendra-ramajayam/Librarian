import sys
import os
import string
from random import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
    QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QAction,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QHeaderView, QLabel, QTreeWidget, QTreeWidgetItem, QToolBar, QLineEdit,
    QCompleter, QSizePolicy, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QStringListModel, QRect, QSize, Qt
import sqlite3
from sqlite3 import Error

from DatabaseIO import *

class GroupTrees(QWidget):
    updateRefsTableSignal = pyqtSignal()
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()
    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.initLocalLib()
        self.initShowingMethod()
        self.initGroups()
        self.initOnlineSearch()
        # Add trees to widget
        self.layout.addWidget(self.localLibTree)
        self.layout.addWidget(self.localGroupTree)
        #self.layout.addWidget(self.showingMethodComboBox)
        self.layout.addLayout(self.methodLayout)
        self.layout.addWidget(self.searchMethodTree)
        self.setLayout(self.layout)

    def initLocalLib(self):
        self.localLibTree = QTreeWidget()
        self.localLibTree.setStyleSheet("max-height: 100px")
        self.localLibTree.setHeaderLabels(["Local Library"])
        localLib1 = QTreeWidgetItem(self.localLibTree, ["All References"])
        localLib2 = QTreeWidgetItem(self.localLibTree, ["Recently Added"])
        localLib3 = QTreeWidgetItem(self.localLibTree, ["Trash"])
        localLib4 = QTreeWidgetItem(self.localLibTree, ["Search"])

        self.localLibTree.setCurrentItem(localLib1)

    def initShowingMethod(self):
        self.methodLabel = QLabel("Show by:")
        self.methodCB = QComboBox()
        self.methodCB.addItems(["Published In", "Label", "Year", "Published In + Year", "Year + Published In"])
        self.methodLayout = QHBoxLayout()
        self.methodLayout.addWidget(self.methodLabel)
        self.methodLayout.addWidget(self.methodCB)
        self.methodCB.currentIndexChanged.connect(self.showingMethodChange)

    def initGroups(self):
        self.localGroupTree = QTreeWidget()
        self.localGroupTree.setHeaderLabels(["My Groups"])
        self.showingMethodInd = 0
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data.db")
        # create a database connection
        groups = []
        try:
            self.conn = createConnectionToDB(database)
            groups = self.getGroupData()
        except:
            buttonReply = QMessageBox.critical(self, 'Alert', "Database is missing", QMessageBox.Ok, QMessageBox.Ok)
        self.setGroups(groups)

    def initOnlineSearch(self):
        self.searchMethodTree = QTreeWidget()
        self.searchMethodTree.setHeaderLabels(["Online Search"])
        searchMethod = []
        defaultSearchMethodList = ["Mixed Search", "Google Scholar", "PubMed", "IEEE Xplore", "Science Direct", "arXiv", "Sci-Hub", "More..."]
        for i in range(len(defaultSearchMethodList)):
            searchMethod.append( QTreeWidgetItem(self.searchMethodTree, [defaultSearchMethodList[i]]) )

    def showingMethodChange(self, i):
        self.showingMethodInd = i
        #print(i, self.methodCB.currentText())
        groups = self.getGroupData()
        self.setGroups(groups)

    def getGroupData(self):
        # Read group names from DataBase
        groupRows = self.readGroupsFromDB(self.conn)
        return groupRows

    def readGroupsFromDB(self, conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        retRows = []
        cur = conn.cursor()
        if self.showingMethodInd == 0:
            try:
                cur.execute("SELECT * FROM PubIn")
                rows = cur.fetchall()
                retRows = rows
            except:
                pass
        elif self.showingMethodInd == 1:
            try:
                cur.execute("SELECT * FROM Labels")
                rows = cur.fetchall()
                retRows = rows
            except:
                pass
        elif self.showingMethodInd == 2:
            try:
                cur.execute("SELECT * FROM Years")
                rows = cur.fetchall()
                retRows = rows
            except:
                pass
        elif self.showingMethodInd == 3:
            """
            PubIn + Years
            """
            try:
                cur.execute("SELECT * FROM PubIn")
                rows1 = cur.fetchall()
                cur.execute("SELECT * FROM Years")
                rows2 = cur.fetchall()
                for pubTerm in rows1:
                    retRows.append((pubTerm[0], pubTerm[1], rows2))
            except:
                pass
        elif self.showingMethodInd == 4:
            """
            Year + PubIn
            """
            try:
                cur.execute("SELECT * FROM Years")
                rows1 = cur.fetchall()
                cur.execute("SELECT * FROM PubIn")
                rows2 = cur.fetchall()
                for yearTerm in rows1:
                    retRows.append((yearTerm[0], yearTerm[1], rows2))
            except:
                pass
        else:
            pass
        return retRows

    def setGroups(self, groups):
        self.localGroupTree.clear()
        roots = []
        for i in range(len(groups)):
            try:
                roots.append( QTreeWidgetItem(self.localGroupTree, [groups[i][1]]) )
                children = []
                for j in range(len(groups[i][2])):
                    tempChild = QTreeWidgetItem()
                    tempChild.setText(0, groups[i][2][j][1])
                    children.append(tempChild)
                roots[i].addChildren(children)
            except:
                pass

    def getSearchMethodData(self):
        # Read search methods from database
        pass
