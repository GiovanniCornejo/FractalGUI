from PySide2.QtWidgets import QApplication

import sys

from wsl import set_display_to_host
from fracviz import FractalApp

def main():
    set_display_to_host()
    app = QApplication(sys.argv)
    fractal_app = FractalApp("data/fracviz.ui")
    fractal_app.root_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()