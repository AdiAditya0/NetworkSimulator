import sys
from PyQt5.QtCore import Qt, QEvent, QObject, QRect, QPropertyAnimation
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QFont
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QApplication, QFrame, QLabel, QSizePolicy, QPushButton, QLineEdit
import tkinter
import time
import threading
import os

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
width = width -100


class paintArea(QWidget):
    x = width * 1.25 / 3
    mid = width * 1.25 / 2
    a = x - 25
    b = 40
    x1 = 2 * x - 25
    y1 = 100
    hposition = 0
    hwidget = height * 1.25
    screen = 1
    totFrames = 0
    labelsLeft = []
    labelsRight = []
    timerOn = False
    curFrame = 0
    finalFrames = 0
    btClick = True
    doSend = []
    dropACK = []
    check = 2
    cur = 0
    nextFrame = 0
    tt = 0
    tp = 0
    count = 0
    increase = 0
    reset = False

    def __init__(self):
        super(paintArea, self).__init__()

        self.ll1 = QLabel(self)
        self.ll1.setGeometry(width + 150, 30, 150, 30)
        self.ll1.setText("Frames")
        self.ll2 = QLabel(self)
        self.ll2.setGeometry(width + 150, 80, 150, 30)
        self.ll2.setText("tp (in ms)")
        self.ll3 = QLabel(self)
        self.ll3.setGeometry(width + 150, 130, 150, 30)
        self.ll3.setText("tt (in ms)")
        self.ll4 = QLabel(self)
        self.ll4.setGeometry(width + 150, 180, 150, 30)
        self.ll4.setText("Bandwidth (in bps)")
        self.ll5 = QLabel(self)
        self.ll5.setGeometry(width + 150, 230, 150, 30)
        self.ll5.setText("ACk to drop")
        self.ll6 = QLabel(self)
        self.ll6.setGeometry(width + 150, 280, 135, 30)
        self.ll6.setText("Frames to drop")

        self.setButton = QPushButton('Set', self)
        self.setButton.setGeometry(width + 300, 330, 100, 30)
        self.setButton.clicked.connect(self.input)

        self.frameLine = QLineEdit(self)
        self.frameLine.setPlaceholderText('Set number of frames')
        self.frameLine.setGeometry(width + 265, 30, 135, 30)

        self.tpLine = QLineEdit(self)
        self.tpLine.setPlaceholderText('Set Propagation delay')
        self.tpLine.setGeometry(width + 265, 80, 135, 30)

        self.ttLine = QLineEdit(self)
        self.ttLine.setPlaceholderText('Set Transmission delay')
        self.ttLine.setGeometry(width + 265, 130, 135, 30)

        self.bwLine = QLineEdit(self)
        self.bwLine.setPlaceholderText('Set Bandwidth')
        self.bwLine.setGeometry(width + 265, 180, 135, 30)

        self.dos = QLineEdit(self)
        self.dos.setPlaceholderText('Ack to drop')
        self.dos.setGeometry(width + 265, 230, 135, 30)

        self.dropa = QLineEdit(self)
        self.dropa.setPlaceholderText('Frames to drop')
        self.dropa.setGeometry(width + 265, 280, 135, 30)

        self.formula = QLabel(self)
        self.formula.setGeometry(width +100 , 380, 350, 175)
        self.formula.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/form.png)")

        self.eff = QLabel(self)
        self.eff.setGeometry(width + 200, 560, 135, 30)
        self.eff.setText("Efficiency = ")
        self.eff1 = QLabel(self)
        self.eff1.setGeometry(width + 200, 610, 135, 30)

        self.through = QLabel(self)
        self.through.setGeometry(width + 200, 660, 135, 30)
        self.through.setText("Troughput (in bps)= ")
        self.through1 = QLabel(self)
        self.through1.setGeometry(width + 200, 710, 135, 30)

        self.res = QPushButton('Reset', self)
        self.res.setGeometry(width + 300, 760, 100, 30)
        self.res.clicked.connect(self.resett)

        self.frame = QLabel(self)
        newfont1 = QFont("Times", 8, QFont.Bold)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
        self.frame.setText("0\nFrame")
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setAlignment(Qt.AlignCenter)
        self.frame.setFont(newfont1)
        self.frame.setGeometry(self.x - 25, 40, 50, 35)

        self.threadList = []

        self.but = QPushButton('Send', self)
        self.but.clicked.connect(self.controller)
        self.but.move(self.x - 400, 40)
        self.but.hide()

        Sender = QLabel('Sender', self)
        Sender.setFrameStyle(QFrame.Panel | QFrame.Raised)
        Sender.setGeometry(self.x - 85, 0, 80, 35)
        Sender.setAlignment(Qt.AlignCenter)
        newfont = QFont("Times", 10, QFont.Bold)
        Sender.setFont(newfont)

        Reciever = QLabel('Receiver', self)
        Reciever.setFrameStyle(QFrame.Panel | QFrame.Raised)
        Reciever.setGeometry(self.x * 2 + 5, 0, 80, 35)
        Reciever.setAlignment(Qt.AlignCenter)
        Reciever.setFont(newfont)

        self.timeLabel = QLabel("Timer", self)
        self.timeLabel.setGeometry(50, 50, 50, 50)
        self.timeLabel.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.timeLabel.setStyleSheet("background-color: yellow")
        self.timeLabel.setAlignment(Qt.AlignCenter)
        newfont = QFont("Times", 10)
        self.timeLabel.setFont(newfont)

        self.DisLabel()

        self.setMinimumWidth((width+100) * 1.25)
        self.setMinimumHeight(self.hwidget)

        img = QImage('C:/Users/sudee/Pictures/pix.png')
        self.offscreen = QPixmap(img)

    def input(self):
        f = self.frameLine.text()
        tp = self.tpLine.text()
        tt = self.ttLine.text()
        bw = self.bwLine.text()
        if int(f) in range(0, 21) and int(tp) in range(0, 20000) and int(tt) in range(0, 20000) and int(
                bw) in range(0, 20000) and self.reset is False and self.dropa.text() is not '' and self.dos.text() is not '':
            self.doSend = self.dos.text().split(",")
            for i in range(0, len(self.doSend)):
                self.doSend[i] = int(self.doSend[i]) - 1

            self.dropACK = self.dropa.text().split(",")
            for i in range(0, len(self.dropACK)):
                self.dropACK[i] = int(self.dropACK[i]) - 1

            eff = (int(tt) / 1000) / ((int(tt) / 1000) + 2 * (int(tp) / 1000))
            self.eff1.setText(str(eff))
            th = eff * int(bw)
            self.through1.setText(str(th))
            self.but.show()
            self.tt = int(tt) / 1000
            self.tt = int(self.tt)
            self.tp = int(int(tp) / 1000)
            self.totFrames = int(f)
            self.count = 2 * self.tt + 2 * self.tp + 2
            self.finalFrames = self.totFrames + len(self.doSend) + len(self.dropACK)
            self.reset = True



    def resett(self):
        os.execl(sys.executable, os.path.abspath("C:/Users/sudee/Downloads/StopNwA.py"), *sys.argv)

    def controller(self):
        self.but.hide()
        if self.btClick is True and self.curFrame < self.totFrames:

            if self.curFrame in self.doSend:
                self.doSend.remove(self.curFrame)
                self.check = 1
            elif self.curFrame in self.dropACK:
                self.dropACK.remove(self.curFrame)
                self.check = 2
            else:
                self.check = 0

            if self.check is 0 or self.check is 1:
                self.case1()
            elif self.check is 2:
                self.case3()

    def DisLabel(self):
        newfont = QFont("Times", 10, QFont.Bold)
        frame = 0
        l1 = QLabel("Sn", self)
        l1.setGeometry(self.x - 150, 10, 30, 30)
        l1.setFrameStyle(QFrame.Panel | QFrame.Raised)
        l1.setStyleSheet("background-color: white")
        l1.setAlignment(Qt.AlignCenter)
        l1.setFont(newfont)
        self.labelsLeft.append(l1)
        for i in range(0, 7):
            l1 = QLabel("<-", self)
            l1.setGeometry(self.x - 240 + 30 * i, 40, 30, 30)
            l1.setFrameStyle(QFrame.Panel | QFrame.Raised)
            if i in range(1, 3):
                l1.setStyleSheet("background-color: lightgreen")
            else:
                l1.setStyleSheet("background-color: yellow")
            l1.setAlignment(Qt.AlignCenter)
            l1.setFont(newfont)
            if i in range(3, 6):
                l1.setText(str(frame))
                if frame is 0:
                    frame = 1
                else:
                    frame = 0
            self.labelsLeft.append(l1)

        frame = 0
        l1 = QLabel("Rn", self)
        l1.setGeometry(self.x * 2 + 120, 70, 30, 30)
        l1.setFrameStyle(QFrame.Panel | QFrame.Raised)
        l1.setStyleSheet("background-color: white")
        l1.setAlignment(Qt.AlignCenter)
        l1.setFont(newfont)
        self.labelsRight.append(l1)

        for i in range(0, 7):
            l1 = QLabel("<-", self)
            l1.setGeometry(self.x * 2 + 30 + 30 * i, 100, 30, 30)
            l1.setFrameStyle(QFrame.Panel | QFrame.Raised)
            if i in range(1, 3):
                l1.setStyleSheet("background-color: lightgreen")
            else:
                l1.setStyleSheet("background-color: yellow")
            l1.setAlignment(Qt.AlignCenter)
            l1.setFont(newfont)
            if i in range(3, 6):
                l1.setText(str(frame))
                if frame is 0:
                    frame = 1
                else:
                    frame = 0
            self.labelsRight.append(l1)

    def addLabel1(self):
        for i in range(2, 6):
            self.labelsLeft[i].setText(str(self.labelsLeft[i + 1].text()))
        if int(self.labelsLeft[6].text()) is 0:
            self.labelsLeft[6].setText("1")
        else:
            self.labelsLeft[6].setText("0")

    def addLabel2(self):
        for i in range(2, 6):
            self.labelsRight[i].setText(str(self.labelsRight[i + 1].text()))
        if int(self.labelsRight[6].text()) is 0:
            self.labelsRight[6].setText("1")
        else:
            self.labelsRight[6].setText("0")


    def transformLabel(self):
        self.labelsLeft[0].move(self.x - 150, 10 + 120*self.cur)
        self.labelsRight[0].move(self.x * 2 + 120, 70 + 120 * self.cur)
        for i in range(1, 8):
            self.labelsLeft[i].move(self.x - 240 + 30 * (i-1), 40 + 120*self.cur)
            self.labelsRight[i].move(self.x*2 + 30*i, 100 + 120*self.cur)



    def case1(self):
        self.btClick = False
        if (self.hposition > self.hwidget - 500):
            self.screen = self.screen + 1
            self.hwidget = self.hwidget + height
            self.setMinimumHeight(self.hwidget)
        self.timerOn = True
        tt = threading.Thread(target=self.stopwatch, args=(self.count,))
        tt.daemon = True
        tt.start()
        self.threadList.append(tt)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(self.tp*1000)
        self.anim.setStartValue(QRect(self.a, self.b, 50, 35))
        self.anim.setEndValue(QRect(self.x1, self.y1, 50, 35))
        self.anim.start()
        self.anim.finished.connect(self.transform)

    def case1Done(self):
        time.sleep(self.tt)
        self.curFrame = self.curFrame + 1
        self.btClick = True
        if self.increase is 1:
            self.addLabel1()
            self.increase = 0
        else:
            self.addLabel1()
        self.timerOn = False
        self.timeLabel.setText("Done")
        t = self.a
        self.hposition = self.hposition + 60
        self.a = self.x1
        self.x1 = t
        self.b = self.y1
        self.y1 = self.y1 + 60
        self.timeLabel.move(50, self.b)
        self.but.move(self.x - 400, self.b)
        self.cur = self.cur + 1
        self.transformLabel()
        time.sleep(1)
        if self.nextFrame is 0:
            self.frame.setText("1\nFrame")
            self.nextFrame = 1
        else:
            self.frame.setText("0\nFrame")
            self.nextFrame = 0
        self.but.click()

    def case2Done(self):
        if (self.hposition > self.hwidget - 500):
            self.screen = self.screen + 1
            self.hwidget = self.hwidget + height
            self.setMinimumHeight(self.hwidget)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/messdrop.png)")
        self.hposition = self.hposition + 60
        self.a = self.x - 25
        self.x1 = self.x * 2 - 25
        self.b = self.y1
        self.y1 = self.y1 + 60

    def case2DD(self):
        self.btClick = True
        self.increase = 1
        self.timeLabel.move(50, self.b)
        self.but.move(self.x - 400, self.b)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
        self.frame.move(self.a, self.b)
        self.cur = self.cur+1
        self.transformLabel()
        if self.nextFrame is 0:
            self.frame.setText("0\nFrame")
        else:
            self.frame.setText("1\nFrame")
            time.sleep(1)
        self.but.click()

    def case3(self):
        self.btClick = False
        if (self.hposition > self.hwidget - 500):
            self.screen = self.screen + 1
            self.hwidget = self.hwidget + height
            self.setMinimumHeight(self.hwidget)
        self.timerOn = True
        tt = threading.Thread(target=self.stopwatch, args=(self.count,))
        tt.daemon = True
        tt.start()
        self.threadList.append(tt)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(self.tp*1000)
        self.anim.setStartValue(QRect(self.a, self.b, 50, 35))
        self.anim.setEndValue(QRect(self.mid, self.y1, 50, 35))
        self.anim.start()
        self.anim.finished.connect(self.transformDrop)

    def transformDrop(self):
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/messdrop.png)")
        self.hposition = self.hposition + 60
        self.a = self.x - 25
        self.x1 = self.x * 2 - 25
        self.b = self.y1 + 60
        self.y1 = self.y1 + 120

    def case3DD(self):
        self.btClick = True
        self.timeLabel.move(50, self.b)
        self.but.move(self.x - 400, self.b)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
        self.frame.move(self.a, self.b)
        self.cur = self.cur+1
        self.transformLabel()
        time.sleep(1)
        if self.nextFrame is 0:
            self.frame.setText("0\nFrame")
        else:
            self.frame.setText("1\nFrame")
        time.sleep(1)
        self.but.click()

    def transform(self):
        if (self.check is 0):
            if self.nextFrame is 0:
                self.frame.setText("1\nAck")
            else:
                self.frame.setText("0\nAck")
            self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
            t = self.a
            self.hposition = self.hposition + 60
            self.a = self.x1
            self.x1 = t
            self.b = self.y1
            self.y1 = self.y1 + 60
            self.timeLabel.move(50, self.b)
            time.sleep(self.tt)
            if self.increase is not 1:
                self.addLabel2()
            self.anim = QPropertyAnimation(self.frame, b"geometry")
            self.anim.setDuration(self.tp*1000)
            self.anim.setStartValue(QRect(self.a, self.b, 50, 35))
            self.anim.setEndValue(QRect(self.x1, self.y1, 50, 35))
            self.anim.start()
            self.anim.finished.connect(self.case1Done)
        elif self.check is 1:
            if self.nextFrame is 0:
                self.frame.setText("1\nAck")
            else:
                self.frame.setText("0\nAck")
            self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/messack.png)")
            self.hposition = self.hposition + 60
            self.a = self.x1
            self.x1 = self.mid
            self.b = self.y1
            self.y1 = self.y1 + 60
            self.timeLabel.move(50, self.b)
            time.sleep(self.tt)
            self.addLabel2()
            self.anim = QPropertyAnimation(self.frame, b"geometry")
            self.anim.setDuration(self.tp*1000)
            self.anim.setStartValue(QRect(self.a, self.b, 50, 35))
            self.anim.setEndValue(QRect(self.x1, self.y1, 50, 35))
            self.anim.start()
            self.anim.finished.connect(self.case2Done)
        return

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 10, Qt.SolidLine)
        painter.setPen(pen)
        for i in range(1, self.screen + 1):
            painter.drawPixmap(0, 1000 * (i - 1), self.offscreen)
            painter.drawLine(self.x, 0, self.x, i * 1000)
            painter.drawLine(self.x * 2, 0, self.x * 2, i * 1000)
        painter.end()
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.gray, 1, Qt.DashLine)
        painter.setPen(pen)
        for i in range(0, self.finalFrames):
            ii = int(i)
            painter.drawLine(self.x, 57 + 120 * ii, self.x * 2, 117 + 120 * ii)
        for i in range(0, self.finalFrames):
            ii = int(i)
            painter.drawLine(self.x * 2, 117 + 120 * ii, self.x, 177 + 120 * ii)
        painter.end()


    def stopwatch(self, seconds):
        ii = 0
        self.timeLabel.setStyleSheet("background-color: yellow")
        for i in range(0, seconds + 1):
            if self.timerOn is False:
                break
            ii = int(i)
            if self.count-ii < 3:
                self.timeLabel.setStyleSheet("background-color: red")
            self.timeLabel.setText(str(seconds - i))
            time.sleep(0.95)
        self.timeLabel.setText("Done")
        if ii is seconds and self.check is 1:
            self.timeLabel.setText("Expire")
            self.timerOn = False
            self.case2DD()
        elif ii is seconds and self.check is 2:
            self.timeLabel.setText("Expire")
            self.timerOn = False
            self.case3DD()



class scrollArea(QWidget):
    def __init__(self):
        super(scrollArea, self).__init__()
        self.showMaximized()
        self.scrollArea = QScrollArea(self)

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(False)

        self.paintArea = paintArea()
        self.scrollArea.setWidget(self.paintArea)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scrollArea)


def main():
    app = QApplication(sys.argv)
    ex = scrollArea()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
