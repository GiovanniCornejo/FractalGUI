from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, QObject, Signal, Slot
from PySide2.QtGui import QIntValidator
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
        """
        Constructor for the FractalApp class. The file is used to create the FractalWindow widget.
        This is also responsible for instantiating the Mandelbrot set class using default values from the GUI,
        updating the plotting image, and displaying it.
        
        Parameters:
        file: The relative path to the .UI file to load.
        """
        super().__init__()
        self.root_widget = FractalWindow(file, self)

        # TODO: Instantiate Mandelbrot set

    def update_plot(self):
        """
        Updates the AxesImage instance. It is responsible for ensuring the display is updated
        without locking up the application by creating and starting a non-GUI thread.
        """

        # TODO: Create and start a non-GUI thread for image processing

        pass

    # ----------------------------------- Slots ---------------------------------- #

    def reset_zoom(self):
        """Reset visual and parameters to default."""
        print("TODO: Reset button clicked")

    def update_iterations(self):
        """Update number of iterations on fractal set."""
        print("TODO: Iterations changed")

    def update_processes(self):
        """Update number of processes used to execute tasks."""
        print("TODO: Processes changed")

    def update_resolution_x(self):
        """Update x resolution (in pixels) of the image."""
        print("TODO: Resolution X changed")

    def update_resolution_y(self):
        """Update y resolution (in pixels) of the image."""
        print("TODO: Resolution Y changed")


class FractalWindow(QWidget):
    """
    Derives from QWidget and is responsible for setting up and connecting elements of the GUI.
    """

    def __init__(self, file: str, app: FractalApp):
        """
        Constructor for the FractalWindow class. The file is used to load the UI. 
        This is also responsible for preparing all elements of the GUI.

        Parameters:
        file: The relative path to the .UI file to load.
        app: A reference to the FractalApp instance which called the constructor
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
        
        # Generate tree of widgets and link widget signals to slots with input validators
        self.layout = self.get_child(self.root_widget, QVBoxLayout, "layout")

        self.iterations = self.get_child(self.root_widget, QLineEdit, "iterations")
        self.iterations.editingFinished.connect(app.update_iterations)
        self.iterations.setValidator(QIntValidator(1, 99,  self.iterations))

        self.processes = self.get_child(self.root_widget, QLineEdit, "processes")
        self.processes.editingFinished.connect(app.update_processes)
        self.processes.setValidator(QIntValidator(1, 4,  self.processes))

        self.resolution_x = self.get_child(self.root_widget, QLineEdit, "resolution_x")
        self.resolution_x.editingFinished.connect(app.update_resolution_x)
        self.resolution_x.setValidator(QIntValidator(1, 3840, self.resolution_x))

        self.resolution_y = self.get_child(self.root_widget, QLineEdit, "resolution_y")
        self.resolution_y.editingFinished.connect(app.update_resolution_y)
        self.resolution_y.setValidator(QIntValidator(1, 2160, self.resolution_y))

        self.reset_button = self.get_child(self.root_widget, QPushButton, "reset_button")
        self.reset_button.clicked.connect(app.reset_zoom)

        self.status = self.get_child(self.root_widget, QLabel, "status")

        # Instantiate FigureCanvas object by creating a Figure and generating an Axes set
        subplot = pyplot.subplots(1)
        self.figure = subplot[0]
        self.axes: Axes = subplot[1]
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def get_child(self, parent, widget_type, widget_name):
        """Helper function for retrieving child widgets"""
        widget = parent.findChild(widget_type, widget_name)
        if isinstance(widget, widget_type):
            return widget
        else:
            print(f"Error: Widget '{widget_name}' not found or of incorrect type.")
            sys.exit(-1)