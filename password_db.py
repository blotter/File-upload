#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import hashlib
import sqlite3
from PyQt4 import QtGui
from PyQt4 import QtCore

class PasspharseDialog(QtGui.QWidget):
    def __init__(self):
        super(PasspharseDialog, self).__init__()
        self.initUI()
        
    def initUI(self):      
        salt = "fr88dlNZkJwE"
        text, ok = QtGui.QInputDialog.getText(
                self
                , 'Password'
                , 'Enter your password:'
                , QtGui.QLineEdit.Password)
        
        if ok:
            self.PassWindow = PasswordWindow(
                    'Password Datenbank'
                    , hashlib.sha256(text + salt).hexdigest()
                    , 380
                    , 400
                    #, '/home/janus/Projects/python/password_sqlite3.db'
                    , '~/password_sqlite3.db'
                    )

class PasswordWindow(QtGui.QWidget):

    def __init__(self, title, passw, width, height, filename):
        super(PasswordWindow, self).__init__()
        self.title = title
        self.passw = passw
        self.width = width
        self.heigh = height
        self.filen = filename

        self.sqlite = sqlite3.connect(self.filen)
        self.initUI()

    def initUI(self):
        self.setGeometry(
                self.width
                , self.width
                , self.width
                , self.heigh
                )
        self.setWindowTitle(self.title)

        ## Menu
        _open = QtGui.QAction("Open", self)
        _save = QtGui.QAction("Save", self)

        _exit = QtGui.QAction("Quit", self)
        _exit.setShortcut('Ctrl+Q')
        _exit.setStatusTip('Exit application')
        _exit.triggered.connect(self.close)

        _hilfe = QtGui.QAction("Hilfe!", self)
        _hilfe.setShortcut('Ctrl+H')
        _hilfe.setStatusTip('Help application')
        _hilfe.triggered.connect(self._menuHelp)

        _menuBar = QtGui.QMenuBar()

        _file = _menuBar.addMenu("&File")
        _file.addAction(_open)
        _file.addAction(_save)
        _file.addAction(_exit)

        _help = _menuBar.addMenu("&Help")
        _help.addAction(_hilfe)

        ## tabss
        _tabWidget = QtGui.QTabWidget()

        self._tab1 = QtGui.QWidget()
        self._tab2 = QtGui.QWidget()

        _tabWidget.addTab(self._tab1, "Erstes")
        _tabWidget.addTab(self._tab2, "Zweites")

        self._tabGen1()

        self._tabGen2()
        #_tab2Vertical.addWidget(self._tabGen2())

        _vbox = QtGui.QVBoxLayout()
        _vbox.addWidget(_menuBar)
        _vbox.addWidget(_tabWidget)
        self.setLayout(_vbox)

        # signals
        QtCore.QObject.connect(_tabWidget, QtCore.SIGNAL('currentChanged(int)'), self._changeTab)
        QtCore.QObject.connect(self._okButton, QtCore.SIGNAL('clicked()'), self._buttonOk)
        QtCore.QObject.connect(self._cancelButton, QtCore.SIGNAL('clicked()'), self._buttonCancel)

        # and action
        self.show()

    def _getDataFromDatabase(self):
        try:
            conn = self.sqlite.cursor()
            _rows = conn.execute('''
                    SELECT 
                        Benutzer
                        , Passwort
                        , Bemerkung 
                    FROM 
                        password 
                    ORDER BY 
                        ID
                    ''')
        except sqlite3.OperationalError:
            print("Database not available, try to create")
            try:
                conn.execute('''CREATE TABLE password
                    (id INTEGER PRIMARY KEY, Benutzer TEXT, Passwort TEXT, Bemerkung TEXT)''')
                conn.execute("INSERT INTO password VALUES (NULL, 'test', 'test', 'test')")
                self.sqlite.commit()
                _rows = conn.execute('''
                        SELECT 
                            Benutzer
                            , Passwort
                            , Bemerkung 
                        FROM
                            password 
                        ORDER BY 
                            id
                        ''')
            except:
                print("Someting went wrong ;)!")
                
        finally:
            self.output = _rows.fetchall()
            conn.close()
            #return output

    def _insetDataToDatabase(self):
        try: 
            conn = self.sqlite.cursor()
        except:
            print("Oops!")

    def _changeTab(self, index):
        print index
        if index == 0:
            self._tabGen1()
        elif index == 1:
            self._userInput.setText("")
            self._passInput.setText("")
            self._descInput.setText("")

    def _buttonOk(self):
        print "User: " + self._userInput.text()
        print "Pass: " + self._passInput.text()
        print "Desc: " + self._descInput.toPlainText()

    def _buttonCancel(self):
        self._userInput.setText("")
        self._passInput.setText("")
        self._descInput.setText("")

    def _tabGen2(self):
        self._tab2Vertical = QtGui.QGridLayout(self._tab2)
        self._tab2Vertical.setSpacing(10)

        _userLabel = QtGui.QLabel('Benutzer:')
        _passLabel = QtGui.QLabel('Passwort:')
        _descLabel = QtGui.QLabel('Bemerkung:')

        self._userInput = QtGui.QLineEdit()
        self._passInput = QtGui.QLineEdit()
        self._descInput = QtGui.QTextEdit()

        self._okButton = QtGui.QPushButton("OK")
        self._cancelButton = QtGui.QPushButton("Cancel")

        self._tab2Vertical.addWidget(_userLabel, 1, 0)
        self._tab2Vertical.addWidget(self._userInput, 1, 1)

        self._tab2Vertical.addWidget(_passLabel, 2, 0)
        self._tab2Vertical.addWidget(self._passInput, 2, 1)

        self._tab2Vertical.addWidget(_descLabel, 3, 0)
        self._tab2Vertical.addWidget(self._descInput, 3, 1, 5, 1)

        self._tab2Vertical.addWidget(self._okButton, 10, 0)
        self._tab2Vertical.addWidget(self._cancelButton, 10, 1)

    def _tabGen1(self):
        self._tab1Vertical = QtGui.QVBoxLayout(self._tab1)
        self._getDataFromDatabase()
        rows = self.output
        print len(rows)
        print range(0, len(rows[0]))
        print rows
        _headers = ["Benutzer", "Password", "BEMERKUNG"]
        self._dataGrid = QtGui.QTableWidget()
        self._dataGrid.setRowCount(len(rows))
        self._dataGrid.setColumnCount(len(_headers))
        self._dataGrid.setAlternatingRowColors(True)
        self._dataGrid.setHorizontalHeaderLabels(_headers)
        n = 0
        for key in range(0, len(rows)):
        #for key in content:
            m = 0
            for item in rows[key]:
                print(n, m, item)
                self._dataGrid.setItem(n, m, QtGui.QTableWidgetItem(item))
                m += 1
            n += 1

        # set table width
        self._dataGrid.resizeColumnsToContents()

        self._dataGrid
        self._tab1Vertical.addWidget(self._dataGrid)

    def _menuHelp(self):
        QtGui.QMessageBox.information(
                self
                , "Dies ist die Hilfe"
                , "Hilf dir selbst, sonst hilft dir keiner!"
                )

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(
                self
                , 'Message'
                , "Are you sure to quit?"
                , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
                , QtGui.QMessageBox.No
                )
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        print(event, event.key())

    def mousePressEvent(self, event):
        print(event, event.key())

def main():

    app = QtGui.QApplication(sys.argv)
    pd = PasspharseDialog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
