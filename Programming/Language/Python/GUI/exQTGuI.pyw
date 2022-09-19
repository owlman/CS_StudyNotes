#! /usr/bin/env python
'''
    Created on 2009-11-20
    
    @author: lingjie
    @name:   example_qtgui
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import * 
import sys

my_array = [['00','01','02'],
            ['10','11','12'],
            ['20','21','22']]

def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.resize(350,150)
    w.show()
    sys.exit(app.exec_())

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        tablemodel = MyTableModel(my_array, self)
        tableview = QTableView()
        tableview.setModel(tablemodel)

        layout = QVBoxLayout(self)
        layout.addWidget(tableview)
        self.setLayout(layout)

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

if __name__ == "__main__":
    main()