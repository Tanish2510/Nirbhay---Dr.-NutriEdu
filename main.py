import sys
import os

# Debugging: Print sys.path to check if the correct directory is include7d 
print("Python search paths before appending:", sys.path)

# Ensure Python finds the correct modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Interface')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Interface', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Interface', 'ui')))

# Debugging: Print sys.path after appending
print("Python search paths after appending:", sys.path)

from Interface.modules.Kiosk import MainApp

from PyQt5 import QtWidgets

def main():
    print("Starting main function")  # Debugging print
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    print("MainApp window shown")  # Debugging print
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 