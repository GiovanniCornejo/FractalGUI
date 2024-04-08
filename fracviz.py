from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, QObject
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import sys


class FractalApp(QObject):
    """
    Derives from QObject and is responsible for storing and updating the 
    fractal set as well as its image representation (AxesImage).
    """

    def __init__(self, file: str):
        # Instantiate fractalwindow from file
        self.root_widget = FractalWindow(file, self) 

    def update_plot(self):
        pass


class FractalWindow(QWidget):
    """
    Derives from QWidget and is responsible for setting up and connecting elements of the GUI.
    """
    def __init__(self, file: str, app: FractalApp):
        """
        Constructor for the FractalWindow class. The file is used to load the UI from the file. 
        This is also responsible for preparing all elements of the GUI.
        """
        super().__init__()

        # Load the UI file with self as the parent of the root widget
        ui_file = QFile(file)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"ERROR: Cannot open {file}: {ui_file.errorString()}")
            sys.exit(-1)
        
        loader = QUiLoader(self)
        self.root_widget = loader.load(ui_file, self)
        ui_file.close()
        if not self.root_widget:
            print(loader.errorString())
            sys.exit(-1)
        
        # Generate tree of widgets
        self.layout = self.get_child(self.root_widget, QVBoxLayout, "layout")
        self.iterations = self.get_child(self.root_widget, QLineEdit, "iterations")
        self.processes = self.get_child(self.root_widget, QLineEdit, "processes")
        self.resolution_x = self.get_child(self.root_widget, QLineEdit, "resolution_x")
        self.resolution_y = self.get_child(self.root_widget, QLineEdit, "resolution_y")
        self.reset_button = self.get_child(self.root_widget, QPushButton, "reset_button")
        self.status = self.get_child(self.root_widget, QLabel, "status")

        # Instantiate FigureCanvas object by creating a Figure and generating an Axes set
        subplot = pyplot.subplots(1)
        self.figure = subplot[0]
        self.axes: Axes = subplot[1]
        self.canvas = FigureCanvas(self.figure)

        # Adding the FigureCanvas object as a child of the layout instance
        self.layout.addWidget(self.canvas)

        # TODO: Link widget signals to slots (methods/functions)

    def get_child(self, parent, widget_type, widget_name):
        widget = parent.findChild(widget_type, widget_name)
        if isinstance(widget, widget_type):
            return widget
        else:
            print(f"Error: Widget '{widget_name}' not found or of incorrect type.")
            sys.exit(-1)