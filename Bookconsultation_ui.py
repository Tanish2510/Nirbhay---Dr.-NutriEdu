from PyQt5.QtWidgets import (QMainWindow, QPushButton, QStackedWidget, QLineEdit,
                             QComboBox, QSpinBox, QRadioButton, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QGroupBox, QApplication, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from Interface.modules.Bookconsultation import NutritionKioskLogic

sys.path.append('c:/Users/soura/WATT/python/Dr-Bharti-KIOSK/Interface')


class NutritionKioskUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = NutritionKioskLogic()  # Create an instance of the logic class
        self.selected_doctor = None  # Initialize selected doctor

        self.setupUi()  # Setup the UI by calling setupUi method
        self.setupUiMainWindow()  # Set up additional main window elements

        # Main Layout
        self.central_widget = QWidget()  # Ensure this is created properly
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Stack widget to manage multiple screens
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Create Patient Information Screen
        self.patient_info_screen = self.create_patient_info_screen()
        self.stack.addWidget(self.patient_info_screen)

        # Create Doctor Selection Screen
        self.doctor_selection_screen = self.create_doctor_selection_screen()
        self.stack.addWidget(self.doctor_selection_screen)

        # Create Confirmation Screen
        self.confirmation_screen = self.create_confirmation_screen()
        self.stack.addWidget(self.confirmation_screen)

    def setupUiMainWindow(self):
        """Set up the main window title and geometry."""
        self.setWindowTitle("Nutrition Kiosk")
        self.setGeometry(100, 100, 800, 600)

    def setupUi(self):
        """Set up the main UI structure."""
        self.setWindowTitle("Nutrition Kiosk")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget and Layout
        self.central_widget = QWidget()  # This ensures QWidget is created correctly
        self.setCentralWidget(self.central_widget)  # Make sure it's set as the central widget
        main_layout = QVBoxLayout(self.central_widget)

    def create_patient_info_screen(self):
        """Creates the patient information screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Title Label
        title_label = QLabel("Patient Information and Consultation Details", self)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Form layout
        form_layout = QGridLayout()

        # Full Name
        form_layout.addWidget(QLabel("Full Name:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Full Name")
        form_layout.addWidget(self.name_input, 0, 1)

        # Phone Number
        form_layout.addWidget(QLabel("Phone Number:"), 1, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter 10-digit Phone Number")
        form_layout.addWidget(self.phone_input, 1, 1)

        # Age
        form_layout.addWidget(QLabel("Age:"), 2, 0)
        self.age_input = QSpinBox()
        self.age_input.setMinimum(1)
        self.age_input.setMaximum(120)
        form_layout.addWidget(self.age_input, 2, 1)

        # Gender GroupBox
        gender_box = QGroupBox("Gender")
        gender_layout = QVBoxLayout()
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.other_radio = QRadioButton("Other")
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addWidget(self.other_radio)
        gender_box.setLayout(gender_layout)
        form_layout.addWidget(gender_box, 3, 0, 1, 2)

        # Child Question GroupBox
        child_box = QGroupBox("Is Patient a Child? (under 18)")
        child_layout = QVBoxLayout()
        self.yes_child_radio = QRadioButton("Yes")
        self.no_child_radio = QRadioButton("No")
        child_layout.addWidget(self.yes_child_radio)
        child_layout.addWidget(self.no_child_radio)
        child_box.setLayout(child_layout)
        form_layout.addWidget(child_box, 4, 0, 1, 2)

        # Nutrition Concern
        form_layout.addWidget(QLabel("Nutrition Concern:"), 5, 0)
        self.problem_combo = QComboBox()
        self.problem_combo.addItems(["Weight Management", "Diabetes", "Heart Health", "General Consultation"])
        form_layout.addWidget(self.problem_combo, 5, 1)

        layout.addLayout(form_layout)

        # Continue Button
        continue_button = QPushButton("Continue to Doctor Selection")
        continue_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; font-weight: bold;")
        continue_button.clicked.connect(self.go_to_doctor_selection)
        layout.addWidget(continue_button)

        # Back to Kiosk Button (Below Continue Button)
        back_to_kiosk_button = QPushButton("Back to Kiosk")
        back_to_kiosk_button.setStyleSheet("background-color: #6c757d; color: white; padding: 10px; font-weight: bold;")
        back_to_kiosk_button.clicked.connect(self.close_booking_chatbot)  # Ensure the button resets the kiosk correctly
        layout.addWidget(back_to_kiosk_button)

        return screen


    def create_doctor_selection_screen(self):
        """Creates the doctor selection screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Title Label
        title_label = QLabel("Select a Doctor")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Instruction Label
        instruction_label = QLabel("Please select a doctor for your consultation:")
        layout.addWidget(instruction_label)

        # Table for doctor selection
        self.doctor_table = QTableWidget()
        self.doctor_table.setColumnCount(3)
        self.doctor_table.setHorizontalHeaderLabels(["Doctor ID", "Name", "Consultation Hours"])
        self.doctor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Detect a row click
        self.doctor_table.cellClicked.connect(self.select_doctor)

        # Add doctor data
        doctors = [
            ("D001", "Dr. Smith", "09:00 - 17:00"),
            ("D003", "Dr. Williams", "08:00 - 16:00")
        ]
        self.doctor_table.setRowCount(len(doctors))

        for row, (doctor_id, name, hours) in enumerate(doctors):
            self.doctor_table.setItem(row, 0, QTableWidgetItem(doctor_id))
            self.doctor_table.setItem(row, 1, QTableWidgetItem(name))
            self.doctor_table.setItem(row, 2, QTableWidgetItem(hours))

        layout.addWidget(self.doctor_table)

        # Navigation Buttons
        button_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; font-weight: bold;")
        back_button.clicked.connect(self.go_to_patient_info)
        button_layout.addWidget(back_button)

        continue_button = QPushButton("Continue")
        continue_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; font-weight: bold;")
        continue_button.clicked.connect(self.save_patient_data)
        button_layout.addWidget(continue_button)

        layout.addLayout(button_layout)

        return screen

    def create_confirmation_screen(self):
        """Creates the confirmation screen."""
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Title Label
        title_label = QLabel("Appointment Confirmation")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Confirmation Details
        self.confirmation_details = QLabel()
        self.confirmation_details.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.confirmation_details)

        # Done Button
        done_button = QPushButton("Done")
        done_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; font-weight: bold;")
        done_button.clicked.connect(self.reset_kiosk)
        layout.addWidget(done_button)

        return screen

    def save_patient_data(self):
        """Saves patient data using logic from NutritionKioskLogic."""
        name = self.name_input.text()
        phone = self.phone_input.text()
        age = self.age_input.value()
        gender = "Male" if self.male_radio.isChecked() else "Female" if self.female_radio.isChecked() else "Other"
        is_child = "Yes" if self.yes_child_radio.isChecked() else "No"
        nutrition_concern = self.problem_combo.currentText()

        # Validate patient info
        valid, message = self.logic.validate_patient_info(name, phone, age)
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        # Save patient data
        patient_data = self.logic.save_patient_data(name, phone, age, gender, is_child, nutrition_concern, self.selected_doctor)

        # Update confirmation details
        confirmation_text = self.logic.generate_confirmation_text(patient_data)
        self.confirmation_details.setText(confirmation_text)

        # Switch to confirmation screen
        self.stack.setCurrentWidget(self.confirmation_screen)

    def select_doctor(self, row, column):
        """Updates the selected doctor based on the row clicked in the table."""
        doctor_id = self.doctor_table.item(row, 0).text()
        doctor_name = self.doctor_table.item(row, 1).text()
        self.selected_doctor = (doctor_id, doctor_name)


    def go_to_patient_info(self):
        """Switches to the patient information screen."""
        self.stack.setCurrentWidget(self.patient_info_screen)

    def go_to_doctor_selection(self):
        """Switches to the doctor selection screen."""
        self.stack.setCurrentWidget(self.doctor_selection_screen)

    def reset_kiosk(self):
        """Resets the kiosk and clears data."""
        self.name_input.clear()
        self.phone_input.clear()
        self.age_input.setValue(1)  # Reset the age input to its minimum value
        self.male_radio.setChecked(False)
        self.female_radio.setChecked(False)
        self.other_radio.setChecked(False)
        self.yes_child_radio.setChecked(False)
        self.no_child_radio.setChecked(False)
        self.problem_combo.setCurrentIndex(0)

        self.stack.setCurrentWidget(self.patient_info_screen)  # Reset the screen back to patient info

    def close_booking_chatbot(self):
        """Closes Nutrition Chatbot and reopens the Kiosk."""
        self.close()  # Close the chatbot
        self.kiosk.show()  # Show the main kiosk window




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NutritionKioskUI()
    window.show()
    sys.exit(app.exec_())
