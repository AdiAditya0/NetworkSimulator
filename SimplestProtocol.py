import sys
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QFont
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QApplication, QFrame, QLabel, QSizePolicy, QPushButton
import tkinter

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


class paintArea(QWidget):
    x = width * 1.25 / 3
    mid = width * 1.25 / 2
    a = x - 25
    b = 40
    x1 = 2 * x - 25
    y1 = 140
    hposition = 0
    hwidget = height*1.25
    screen = 1
    totFrames = 7
    labelsLeft = []
    labelsRight = []

    def __init__(self):
        super(paintArea, self).__init__()

        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-image: url(C:/Users/sudee/Pictures/mess.png)")
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setGeometry(self.x - 25, 40, 50, 35)

        self.but = QPushButton('Send', self)
        self.but.clicked.connect(self.doAnim)
        self.but.move(self.x - 250, 50)

        self.DisLabel()

        self.setMinimumWidth(width*1.25)
        self.setMinimumHeight(self.hwidget)

        img = QImage('C:/Users/sudee/Pictures/pix.png')
        self.offscreen = QPixmap(img)

    def controller(self):
        pass

    def DisLabel(self):
        newfont = QFont("Times", 15, QFont.Bold)
        for i in range(0, self.totFrames):
            l1 = QLabel(str(i+1), self)
            l1.setGeometry(self.x - 150, 40 + 200 * i, 50, 50)
            l1.setFrameStyle(QFrame.Panel | QFrame.Raised)
            l1.setStyleSheet("background-color: yellow")
            l1.setAlignment(Qt.AlignCenter)
            l1.setFont(newfont)
            self.labelsLeft.append(l1)

        for i in range(0, self.totFrames):
            l1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            l1 = QLabel(str(i+1), self)
            l1.setFont(newfont)
            l1.setAlignment(Qt.AlignCenter)
            l1.setGeometry(self.x * 2 + 100, 140 + 200 * i, 50, 50)
            l1.setFrameStyle(QFrame.Panel | QFrame.Raised)
            l1.setStyleSheet("background-color: yellow")
            self.labelsRight.append(l1)


    def doAnim(self):
        if not self.totFrames:
            return
        if(self.hposition > self.hwidget-300):
            self.screen = self.screen + 1
            self.hwidget = self.hwidget + height
            self.setMinimumHeight(self.hwidget)
        self.totFrames = self.totFrames-1
        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(self.a, self.b, 50, 35))
        self.anim.setEndValue(QRect(self.x1, self.y1, 50, 35))
        self.anim.start()
        self.anim.finished.connect(self.transform)

    def transform(self):
        self.hposition = self.hposition + 200
        self.a = self.x - 25
        self.x1 = self.x*2 - 25
        self.b = self.y1+100
        self.y1 = self.y1 + 200
        self.but.move(self.x - 250, self.b)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 10, Qt.SolidLine)
        painter.setPen(pen)
        for i in range(1, self.screen+1):
            painter.drawPixmap(0, 1000 * (i-1), self.offscreen)
            painter.drawLine(self.x, 0, self.x, i*1000)
            painter.drawLine(self.x * 2, 0, self.x * 2, i*1000)
        painter.end()


class scrollArea(QWidget):
    def __init__(self):
        super(scrollArea, self).__init__()
        self.showMaximized()
        self.scrollArea = QScrollArea(self)

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn )
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
