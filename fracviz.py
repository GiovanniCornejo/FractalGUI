from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice, QObject, Qt, QEvent
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

import sys
from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager
import threading

from fractal import Mandelbrot


class FractalApp(QObject):
    """
    Responsible for storing and updating the fractal set and its image representation.
    """

    def __init__(self, file: str):
        """
        Creates a FractalWindow widget from a .UI file and instantiates the Mandelbrot set 
        using default values from the GUI. The plotting image is updated and displayed.
        
        Parameters:
        `file`: The relative path to the .UI file to load.
        """
        super().__init__()
        
        self._root_widget = FractalWindow(file, self)
        
        # Store defaults
        self._def_iterations = self._root_widget.iterations.text()
        self._def_processes = self._root_widget.processes.text()
        self._def_resolution_x = self._root_widget.resolution_x.text()
        self._def_resolution_y = self._root_widget.resolution_y.text()

        self._image = None
        self._fractal = Mandelbrot(
            int(self._def_resolution_x),
            int(self._def_resolution_y),
            int(self._def_iterations)
        )
        
        self.update_plot()

    def update_plot(self):
        """
        Updates the display via the AxesImage instance by creating and starting a non-GUI thread to
        prevent the application from locking up.
        """
        self._root_widget.status.setText("Calculating set...")

        # Create and start a non-GUI thread for image processing so that the GUI does not freeze
        def process_image():
            num_tasks = int(self._root_widget.processes.text())
            with SharedMemoryManager() as smm:
                tasks, data = self._fractal.generate_tasks(smm, num_tasks)

            # Create and start appropriate number of processes to execute tasks.
            processes = [Process(target=task) for task in tasks]
            for p in processes:
                p.start()
            for p in processes:
                p.join()

            # Get updated image data and update the AxesImage object.
            image_matrix = self._fractal.data_to_image_matrix(data)
            if self._image is None:
                self._image = self._root_widget.axes.imshow(image_matrix)
                self._root_widget.status.setText("")
                self._root_widget.canvas.draw()
                self._def_xlim = self._root_widget.canvas.figure.gca().get_xlim()
                self._def_ylim = self._root_widget.canvas.figure.gca().get_ylim()
            else:
                self._image.set_data(image_matrix)
                self._root_widget.status.setText("")
                self._root_widget.canvas.draw()

        threading.Thread(target=process_image, daemon=True).start()

    def update_iterations(self):
        """Update the plot with the changed iterations count."""
        self._fractal.iterations = int(self._root_widget.iterations.text())
        self.update_plot()

    def update_resolution_x(self):
        """Update the plot with the changed resolution x."""
        self._fractal.dimensions = (int(self._root_widget.resolution_x.text()), self._fractal.dimensions[1])
        self.update_plot()

    def update_resolution_y(self):
        """Update the plot with the changed resolution y."""
        self._fractal.dimensions = (self._fractal.dimensions[0], int(self._root_widget.resolution_y.text()))
        self.update_plot()

    def reset(self):
        """Reset visuals and parameters to default values then update plot."""
        self._root_widget.iterations.setText(self._def_iterations)
        self._root_widget.processes.setText(self._def_processes)
        self._root_widget.resolution_x.setText(self._def_resolution_x)
        self._root_widget.resolution_y.setText(self._def_resolution_y)

        self._fractal.iterations = int(self._def_iterations)
        self._fractal.dimensions = (int(self._def_resolution_x), int(self._def_resolution_y))

        self._root_widget.canvas.figure.gca().set_xlim(self._def_xlim)
        self._root_widget.canvas.figure.gca().set_ylim(self._def_ylim)
        self._root_widget.canvas.draw()

        self.update_plot()

    # --------------------------------- Accessors -------------------------------- #

    @property
    def fractal(self):
        return self._fractal

    @property
    def image(self):
        return self._image
    
    @property
    def root_widget(self):
        return self._root_widget

# ---------------------------------------------------------------------------- #

class FractalWindow(QWidget):
    """
    Derives from QWidget and is responsible for setting up and connecting elements of the GUI.
    """

    def __init__(self, file: str, app: FractalApp):
        """
        Constructor for the FractalWindow class. The file is used to load the UI. 
        This is also responsible for preparing all elements of the GUI.

        Parameters:
        `file`: The relative path to the .UI file to load.
        `app`: A reference to the FractalApp instance which called the constructor
        """
        super().__init__()

        # Load the UI file with self as the parent of the root widget
        ui_file = QFile(file)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"ERROR: Cannot open {file}: {ui_file.errorString()}")
            sys.exit(-1)
        
        loader = QUiLoader()
        if not loader.load(ui_file, self):
            print(loader.errorString())
            sys.exit(-1)
        ui_file.close()
        
        # Generate tree of widgets and link widget signals to slots with input validators
        self.layout = self.get_child(self, QVBoxLayout, "layout")

        self.iterations = self.get_child(self, QLineEdit, "iterations")
        self.iterations.returnPressed.connect(app.update_iterations)
        self.iterations.setValidator(QIntValidator(1, 99,  self.iterations))

        self.processes = self.get_child(self, QLineEdit, "processes")
        self.processes.returnPressed.connect(app.update_plot)
        self.processes.setValidator(QIntValidator(1, 99,  self.processes))

        self.resolution_x = self.get_child(self, QLineEdit, "resolution_x")
        self.resolution_x.returnPressed.connect(app.update_resolution_x)
        self.resolution_x.setValidator(QIntValidator(1, 4096, self.resolution_x))

        self.resolution_y = self.get_child(self, QLineEdit, "resolution_y")
        self.resolution_y.returnPressed.connect(app.update_resolution_y)
        self.resolution_y.setValidator(QIntValidator(1, 2160, self.resolution_y))

        self.reset_button = self.get_child(self, QPushButton, "reset_button")
        self.reset_button.pressed.connect(app.reset)

        self.status = self.get_child(self, QLabel, "status")

        # Instantiate FigureCanvas object by creating a Figure and generating an Axes set
        self.figure, self.axes = pyplot.subplots(1)
        self.axes.set_position([0,0,1,1]) # Position and size axes to fill entire figure
        self.axes.set_axis_off() # Turn off axis information
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Add mouse click-and-drag operations to facilitate zoom functionality
        self.eventfilter = EventFilter(self.canvas)
        self.canvas.installEventFilter(self.eventfilter)

    def get_child(self, parent, widget_type, widget_name):
        """Helper function for retrieving child widgets"""
        widget = parent.findChild(widget_type, widget_name)
        if isinstance(widget, widget_type):
            return widget
        else:
            print(f"Error: Widget '{widget_name}' not found or of incorrect type.")
            sys.exit(-1)

class EventFilter(QObject):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.start_mouse_pos = None

    def eventFilter(self, obj, event):
        if obj and obj == self.canvas:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.left_mouse_pressed = True
                    self.start_mouse_pos = event.pos()
                elif event.button() == Qt.RightButton:
                    self.right_mouse_pressed = True
                    self.start_mouse_pos = event.pos()
            elif event.type() == QEvent.Type.MouseMove:
                if self.left_mouse_pressed:
                    delta = event.pos() - self.start_mouse_pos
                    self.zoom(delta)
                    self.start_mouse_pos = event.pos()
                elif self.right_mouse_pressed:
                    delta = event.pos() - self.start_mouse_pos
                    self.pan(delta)
                    self.start_mouse_pos = event.pos()
            elif event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.LeftButton and self.left_mouse_pressed:
                    delta = event.pos() - self.start_mouse_pos
                    self.zoom(delta)
                    self.left_mouse_pressed = False
                elif event.button() == Qt.RightButton and self.right_mouse_pressed:
                    delta = event.pos() - self.start_mouse_pos
                    self.pan(delta)
                    self.right_mouse_pressed = False

        return False
    
    def zoom(self, delta):
        """Zoom the plot."""
        zoom_speed = 0.001  # Adjust this value to control zoom speed
        zoom_factor = 1.0 + zoom_speed * delta.y()
        zoom_factor = max(0.1, min(zoom_factor, 10.0))  # Limit zoom factor within reasonable bounds
        
        # Get current axis limits
        xlim = self.canvas.figure.gca().get_xlim()
        ylim = self.canvas.figure.gca().get_ylim()
        
        # Calculate new axis limits
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        new_width = (xlim[1] - xlim[0]) / zoom_factor
        new_height = (ylim[1] - ylim[0]) / zoom_factor
        new_xlim = [x_center - new_width / 2, x_center + new_width / 2]
        new_ylim = [y_center - new_height / 2, y_center + new_height / 2]
        
        # Set new axis limits
        self.canvas.figure.gca().set_xlim(new_xlim)
        self.canvas.figure.gca().set_ylim(new_ylim)
        
        # Redraw canvas
        self.canvas.draw()

    def pan(self, delta):
        """Pan the plot."""
        # Get current axis limits
        xlim = self.canvas.figure.gca().get_xlim()
        ylim = self.canvas.figure.gca().get_ylim()

        # Calculate the distance covered by the mouse movement
        x_pan_distance = -delta.x() * (xlim[1] - xlim[0]) / self.canvas.width()
        y_pan_distance = delta.y() * (ylim[1] - ylim[0]) / self.canvas.height()

        # Calculate the new axis limits
        new_xlim = [xlim[0] + x_pan_distance, xlim[1] + x_pan_distance]
        new_ylim = [ylim[0] + y_pan_distance, ylim[1] + y_pan_distance]

        # Set new axis limits
        self.canvas.figure.gca().set_xlim(new_xlim)
        self.canvas.figure.gca().set_ylim(new_ylim)

        # Redraw canvas
        self.canvas.draw()
