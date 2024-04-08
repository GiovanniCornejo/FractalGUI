from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject

import sys

from fractal import Mandelbrot
from fractalwindow import FractalWindow

class FractalApp(QObject):

    def __init__(self, file: str):
        app = QApplication(sys.argv)

        # Instantiate fractalwindow from file
        self.fractal_window = FractalWindow(file, app)

        # Instantiate the Mandelbrot set class using default values from the GUI
        # updating the plotting image, and displaying it in accordance with the rest
        # of the specification


    def update_plot(self):
        # 1) Create and start a non-GUI thread for image processing so that the GUI does not freeze

        # 2) Non-GUI thread should generate the fractal tasks using the process count (see Mandelbrot specification)

        # 3) Non-GUI thread should create the appropriate number of processes to execute tasks

        # 4) The processes should start but take care that no task runs more than once!

        # 5) Non-GUI thread should wait for all tasks to be completed

        # 6) Non-GUI thread should get updated image data and update the AxesImage object

        # 7) Non-GUI thread should get updated image data and update the AxesImage object

        # 8) GUI thread, upon receipt of signal, should update the visualization
        pass