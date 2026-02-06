import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def resource_path(*parts):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, *parts)

def main():
    os.environ["QT_API"] = "pyside6"
    
    app = QApplication(sys.argv)
    
    try:
        theme_path = resource_path("ui", "themes", "y2k.qss")
        with open(theme_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: Theme file not found, loading default.")

    window = MainWindow()
    window.setWindowTitle("Forensic-Amp: Attacker-Aware Log Analyzer")
    window.showMaximized()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
