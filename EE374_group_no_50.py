import sys
from PySide6.QtWidgets import QApplication
from GUI import PowerCableSelectionApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PowerCableSelectionApp()
    window.show()
    sys.exit(app.exec())