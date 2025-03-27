import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QDate
# Get the root directory of the project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from Interface.ui.Bookconsultation_ui import NutritionKioskUI

def main():
    app = QApplication(sys.argv)
    
    # Load CSS style sheet (optional)
    try:
        with open("style.css", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet not found, using default styles.")
    
    # Create and show the kiosk application
    kiosk = NutritionKioskUI()
    
    kiosk.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()