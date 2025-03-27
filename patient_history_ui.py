# patient_ui.py
import sys
import uuid
from PyQt5 import QtWidgets, QtGui, QtCore

class PatientInfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Patient Information")
        self.setGeometry(100, 100, 600, 550)  # Increased height

        # Apply CSS styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QSpinBox, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: #fff;
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #367c39;
            }
        """)

        # Labels and Input Fields
        self.name_label = QtWidgets.QLabel("Patient Name:")
        self.name_input = QtWidgets.QLineEdit()

        self.number_label = QtWidgets.QLabel("Phone Number:")
        self.number_input = QtWidgets.QLineEdit()

        self.uid_label = QtWidgets.QLabel("Patient UID:")
        self.uid_value = QtWidgets.QLineEdit()
        self.uid_value.setReadOnly(True)
        self.generate_uid()

        self.age_label = QtWidgets.QLabel("Age:")
        self.age_spinbox = QtWidgets.QSpinBox()
        self.age_spinbox.setRange(0, 120)

        self.personal_history_label = QtWidgets.QLabel("Personal Medical History:")
        self.personal_history_text = QtWidgets.QTextEdit()

        self.family_history_label = QtWidgets.QLabel("Family Medical History:")
        self.family_history_text = QtWidgets.QTextEdit()

        # Buttons
        self.save_button = QtWidgets.QPushButton("Save")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        # Layout with Spacing and Margins
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        form_layout.addRow(self.name_label, self.name_input)
        form_layout.addRow(self.number_label, self.number_input)
        form_layout.addRow(self.uid_label, self.uid_value)
        form_layout.addRow(self.age_label, self.age_spinbox)
        form_layout.addRow(self.personal_history_label, self.personal_history_text)
        form_layout.addRow(self.family_history_label, self.family_history_text)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(20, 0, 20, 20)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove main layout margins
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Connect Buttons
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def generate_uid(self):
        """Generates a unique patient ID."""
        uid = str(uuid.uuid4())
        self.uid_value.setText(uid)

    def get_patient_info(self):
        """Retrieves patient information from the dialog."""
        return {
            "name": self.name_input.text(),
            "number": self.number_input.text(),
            "uid": self.uid_value.text(),
            "age": self.age_spinbox.value(),
            "personal_history": self.personal_history_text.toPlainText(),
            "family_history": self.family_history_text.toPlainText()
        }


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = PatientInfoDialog()
    result = dialog.exec_()

    if result == QtWidgets.QDialog.Accepted:
        patient_data = dialog.get_patient_info()
        print("Patient Information:")
        for key, value in patient_data.items():
            print(f"{key}: {value}")
    else:
        print("Dialog canceled.")

    sys.exit(app.exec_())
