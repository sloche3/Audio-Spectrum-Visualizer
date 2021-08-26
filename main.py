from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
import pyaudio
import struct
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, middle=True, top=False, bottom=False, topBottom=False, tieDye=True):
        super(MainWindow, self).__init__()

        # might need this for command line args later..
        #    def __init__(self, *args, **kwargs):
        #        super(MainWindow, self).__init__(*args, **kwargs)

        # instantiates a plot widget and sets it as the 'central widget'
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # instantiates pyaudio
        self.p = pyaudio.PyAudio()

        # defines the settings that the pyaudio stream will use
        self.CHUNK = 1024 * 4
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        # opens the pyaudio stream
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # sets background color to black
        self.blk = pg.mkColor(0, 0, 0)
        self.graphWidget.setBackground(self.blk)

        # sets a pen color ot purple
        self.pen = pg.mkPen(color=(195, 0, 255))

        # background color presets (set to dark purple, used if tieDye == True)
        self.bkRed = 39
        self.bkGreen = 2
        self.bkBlue = 51

        # pen color presets (set to light purple)
        self.penRed = 195
        self.penGreen = 0
        self.penBlue = 255

        # determines where the data line will be shown
        self.middle = middle
        self.top = top
        self.bottom = bottom
        self.topBottom = topBottom
        self.tieDye = tieDye

        # if tieDye == False, the background is set to black and the pen is light purple
        self.pen = pg.mkPen(color=(self.penRed, self.penGreen, self.penBlue))
        self.backgroundColor = pg.mkColor(0, 0, 0)
        self.graphWidget.setBackground(self.backgroundColor)

        # sets the range for the graphing widget
        self.graphWidget.setYRange(0, 255, padding=0)
        self.graphWidget.setXRange(0, 1024 * 4, padding=0.005)

        # hides the X and Y axis
        self.graphWidget.hideAxis('bottom')
        self.graphWidget.hideAxis('left')

        # hides window title bar
        # self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # instantiates a timer and sets it to constantly call the update_plot_data function
        self.timer = QtCore.QTimer()
        self.timer.start(0)
        self.timer.timeout.connect(self.Update_plot_data)
        self.timer.start()

    # updates the graph by :
    # 1. clearing whats on the screen
    # 2. reading the audio stream
    # 3. converting that audio to "frequency data" that can be plotted (I think...)
    # 4. plotting that new data
    def Update_plot_data(self):
        self.graphWidget.clear()
        spf = self.stream.read(self.CHUNK)
        wf_data = struct.unpack(str(8 * 1024) + 'B', spf)

        if self.middle:
            topPlot = np.array(wf_data, dtype='b')[::2] + 128
            if self.tieDye:
                self.ColorShift()
            self.data_line = self.graphWidget.plot(topPlot, pen=self.pen)

        elif self.top:
            topPlot = np.array(wf_data, dtype='b')[::] + 256
            if self.tieDye:
                self.ColorShift()
            self.data_line = self.graphWidget.plot(topPlot, pen=self.pen)

        elif self.bottom:
            bottomPlot = np.array(wf_data, dtype='b')[::] + 0
            if self.tieDye:
                self.ColorShift()
            self.data_line = self.graphWidget.plot(bottomPlot, pen=self.pen)

        elif self.topBottom:
            topPlot = np.array(wf_data, dtype='b')[::] + 256
            bottomPlot = np.array(wf_data, dtype='b')[::] + 0
            if self.tieDye:
                self.ColorShift()
            self.data_line = self.graphWidget.plot(topPlot, pen=self.pen)
            self.data_line = self.graphWidget.plot(bottomPlot, pen=self.pen)

    # used to change background and pen colors if tieDye == True
    def ColorShift(self):
        if self.bkRed == 51 and self.bkGreen == 2:
            if self.bkBlue == 2:
                self.bkGreen += 1
                self.penGreen += 5
            else:
                self.bkBlue -= 1
                self.penBlue -= 5

        elif self.bkRed == 2 and self.bkGreen == 51:
            if self.bkBlue == 51:
                self.bkGreen -= 1
                self.penGreen -= 5
            else:
                self.bkBlue += 1
                self.penBlue += 5

        elif self.bkRed == 51 and self.bkBlue == 2:
            if self.bkGreen == 51:
                self.bkRed -= 1
                self.penRed -= 5
            else:
                self.bkGreen += 1
                self.penGreen += 5

        elif self.bkRed == 2 and self.bkBlue == 51:
            if self.bkGreen == 2:
                self.bkRed += 1
                self.penRed += 5
            else:
                self.bkGreen -= 1
                self.penGreen -= 5

        elif self.bkBlue == 2 and self.bkGreen == 51:
            if self.bkRed == 2:
                self.bkBlue += 1
                self.penBlue += 5
            else:
                self.bkRed -= 1
                self.penRed -= 5

        elif self.bkBlue == 51 and self.bkGreen == 2:
            if self.bkRed == 51:
                self.bkBlue -= 1
                self.penBlue -= 5
            else:
                self.bkRed += 1
                self.penRed += 5

        self.pen = pg.mkPen(color=(self.penRed, self.penGreen, self.penBlue))
        self.backgroundColor = pg.mkColor(self.bkRed, self.bkGreen, self.bkBlue)
        self.graphWidget.setBackground(self.backgroundColor)


# main
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()

# stops the graph window from closing automatically (for some reason..)
app.exec()
