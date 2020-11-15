#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import sys
import time
from PySide import QtGui,QtCore
import threading
from PySide.QtCore import QTimer

class SignalHelper(QtCore.QObject):
    data_send = QtCore.Signal(object)

class SampleThread(QtCore.QRunnable):
    def __init__(self, data):
        QtCore.QRunnable.__init__(self)
        #Decompress data from string into dictionary
        self.mutate = ast.literal_eval(data)

        self._signal_helper = SignalHelper()
        self.data_send = self._signal_helper.data_send


    def run(self):
        #Start sample Thread
        self.data_send.emit('hello from SampleThread>> Starting !!')
        self.logic()

    def logic(self):
        #Do SampleThread Logic Here
        for x in range(0,10):
            self.mutate['random_number']+=1
            time.sleep(1)
            self.data_send.emit(self.mutate)





class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()


    def starty(self):
        data = {'username':'cats',
                'msg': 'Hi from Main Gui Thread',
                'random_number': 777,
                'thread_number':1
                }


        # we convert the list into a string so the object is not connected in any way then mutate it over with ast
        downloader = SampleThread(str(data))
        downloader.data_send.connect(self.echo)


        self.thread_pool = QtCore.QThreadPool()
        self.thread_pool.setMaxThreadCount(1)
        self.thread_pool.start(downloader)

        self.timer = QTimer()
        self.timer.setInterval(10000) #10 seconds
        self.timer.start()
        self.timer.timeout.connect(self.loop) #call loop every 10 seconds

    def loop(self):
        #Do Gui updating stuff here such as displaying data
        print 'Main Gui Loop every 10 seconds'
        thread_count = str(self.thread_pool.activeThreadCount())
        self.console.addItem(thread_count)


    def initUI(self):
        '''Create GUI stuff here
        Random notes:
        QVBox = Vertical up/down
        QHBox = Horizonal left/right
        self.resize window height/width
        self.console this is our main widget to display data to the gui
        '''

        self.resize(550, 300)

        # QVBox = Vertical up/down
        layout = QtGui.QVBoxLayout()

        self.console = QtGui.QListWidget()
        layout.addWidget(self.console)
        self.console.addItem("Very Basic Gui displaying thread usage using python 2.7/Pyside ")

        btn = QtGui.QPushButton('Button', self)
        btn.clicked.connect(self.starty)

        layout.addWidget(btn)

        self.setLayout(layout)

    def echo(self,payload):
        print 'hi from echo'
        texty = 'payload -> ' + str(payload)
        self.console.addItem(texty)
        self.console.scrollToBottom() #scrolls down





def main():
    app = QtGui.QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()