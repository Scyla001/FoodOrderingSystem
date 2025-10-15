import sys
from PyQt6.QtWidgets import QApplication
from Shell.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
