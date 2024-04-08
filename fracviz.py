from wsl import set_display_to_host

from fractalapp import FractalApp

def main():
    set_display_to_host()

    FractalApp("data/fracviz.ui")

if __name__ == "__main__":
    main()