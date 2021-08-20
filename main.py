from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
import pyaudio
import struct
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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

        # sets the range for the graphing widget
        self.graphWidget.setYRange(0, 255, padding=0)
        self.graphWidget.setXRange(0, 1024 * 4, padding=0.005)

        # instantiates a timer and sets it to constantly call the update_plot_data function
        self.timer = QtCore.QTimer()
        self.timer.start(0)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    # updates the graph by :
    # 1. clearing whats on the screen
    # 2. reading the audio stream
    # 3. converting that audio to "frequency data" that can be plotted (I think...)
    # 4. plotting that new data
    def update_plot_data(self):
        self.graphWidget.clear()
        spf = self.stream.read(self.CHUNK)
        wf_data = struct.unpack(str(8 * 1024) + 'B', spf)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        data_line = self.graphWidget.plot(wf_data, pen=self.pen)


# main
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()

# stops the graph window from closing automatically (for some reason..)
app.exec()
