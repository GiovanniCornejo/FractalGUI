from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtWidgets import QApplication, QWidget

import sys

class FractalWindow(QWidget):
    def __init__(self, file: str, app: QApplication):
        super().__init__()

        # Loading the UI file and generating a tree of widgets from it
        # with self as the parent of the root
        ui_file = QFile(file)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"ERROR: Cannot open {file}: {ui_file.errorString()}")
            sys.exit(-1)
        
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)

        window.show()

        sys.exit(app.exec_())

        # Instantiating a FigureCanvas object, 
        # creating a Figure, and generating an Axes set

        # Adding the FigureCanvas object as a child of the layout instance (see properties)

        # Linking widget signals to slots (methods / functions)

        # Setting up event filters as necessary

        # Any other actions required to faciliate proper application behavior
        pass