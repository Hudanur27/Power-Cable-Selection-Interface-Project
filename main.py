

import os
import sys
import pandas as pd


from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from GUI import PowerCableSelectionApp


def get_resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    # Create splash screen
    try:
        splash_pix = QPixmap("splash.png")  # You'll need to create this image
    except:
        # Create a blank pixmap if splash.png not found
        splash_pix = QPixmap(400, 300)
        splash_pix.fill(Qt.white)
    
    splash = QSplashScreen(splash_pix)
    splash.showMessage("Loading Cable Selection App...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
    splash.show()
    app.processEvents()
    
    # Create main window with a slight delay to show splash screen
    window = PowerCableSelectionApp()
    
    # Close splash and show main window
    QTimer.singleShot(1500, splash.close)
    QTimer.singleShot(1500, window.show)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()