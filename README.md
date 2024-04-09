# Fractal GUI

![Demo](demo/FractalGUI_demo.gif)

## Description

An application to navigate the visualization of the Mandelbrot set via an interactive interface.

**NOTE**: This application is designed and tested specifically for WSL (Windows Subsystem for Linux).

## Usage

After launching the application, you'll encounter a GUI with the following options:

- **X Resolution**: Change the x resolution of the Mandelbrot set.
- **Y Resolution**: Change the y resolution of the Mandelbrot set.
- **Num Passes**: Change the number of iterations done on the Mandelbrot set.
- **Processes**: Change the number of tasks used to generate the Mandelbrot set.

You can also perform the following actions on the Mandelbrot set:

- **Left-click and Drag**: Zoom in and out of the Mandelbrot set.
- **Right-click and Drag**: Pan across the Mandelbrot set.

## Dependencies

- Python 3: Required for running the Python code.
- VcXsrv: An X Server for Windows for displaying graphical applications running in WSL.
- Qt5 GUI system: The GUI framework.
- PySide2: Python binds for the Qt framework, used for creating the GUI.
- Matplotlib: Python plotting library used for visualizing the Mandelbrot set.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GiovanniCornejo/FractalGUI.git
   cd FractalGUI
   ```
2. Run the X server.
3. Run the application:
   ```bash
   python3 main.py
   ```

## License

This project is licensed under the [MIT License](LICENSE).
