from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QMessageBox, QStackedWidget, QFormLayout,
                             QComboBox, QCalendarWidget, QTimeEdit)
from PyQt5.QtCore import Qt, QTime, QDate, QRegExp
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from modules.Commontips import NutritionalHealthBackend
import re
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)


class HealthConsultationKioskUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialization code
        self.setWindowTitle("Nutritional Health Kiosk")
        self.setMinimumSize(800, 600)

        # Initialize the backend
        self.backend = NutritionalHealthBackend()

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create stacked widget to handle different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create different pages
        self.create_welcome_page()
        self.create_health_details_page()
        self.create_recommendations_page()
        self.create_appointment_page()
        self.create_confirmation_page()
        self.create_view_appointments_page()

        # Start with welcome page
        self.stacked_widget.setCurrentIndex(0)

    def create_welcome_page(self):
        welcome_widget = QWidget()
        layout = QVBoxLayout()

        # Welcome message
        welcome_label = QLabel("Welcome to the Nutritional Health Kiosk")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")

        info_label = QLabel("This kiosk will provide nutritional advice based on your health information.\n"
                           "No personal data will be stored.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 16px; margin: 10px;")

        # Start button
        start_button = QPushButton("Start")
        start_button.setFixedSize(200, 50)
        start_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # View Appointments button
        view_appointments_button = QPushButton("View Appointments")
        view_appointments_button.setFixedSize(200, 50)
        view_appointments_button.clicked.connect(self.load_appointments)
        view_appointments_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        # Add widgets to layout
        layout.addStretch()
        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addSpacing(30)
        layout.addWidget(start_button, 0, Qt.AlignCenter)
        layout.addWidget(view_appointments_button, 0, Qt.AlignCenter)
        layout.addStretch()

        welcome_widget.setLayout(layout)
        self.stacked_widget.addWidget(welcome_widget)

    def create_health_details_page(self):
        details_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Enter Your Health Information")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        # Form layout for details
        form_layout = QFormLayout()

        # Age input with validator (integers between 1-120)
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter your age (1-120)")
        age_validator = QIntValidator(1, 120, self)
        self.age_input.setValidator(age_validator)
        form_layout.addRow("Age:", self.age_input)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Select Gender", "Male", "Female", "Other", "Prefer not to say"])
        form_layout.addRow("Gender:", self.gender_input)

        # Height input with validator (integers/decimals between 50-250 cm)
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height in cm (50-250)")
        height_validator = QDoubleValidator(50.0, 250.0, 1, self)
        height_validator.setNotation(QDoubleValidator.StandardNotation)
        self.height_input.setValidator(height_validator)
        form_layout.addRow("Height (cm):", self.height_input)

        # Weight input with validator (integers/decimals between 2-500 kg)
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight in kg (2-500)")
        weight_validator = QDoubleValidator(2.0, 500.0, 1, self)
        weight_validator.setNotation(QDoubleValidator.StandardNotation)
        self.weight_input.setValidator(weight_validator)
        form_layout.addRow("Weight (kg):", self.weight_input)

        # Health description
        description_label = QLabel("Please describe your health concerns, conditions, or symptoms:")
        self.health_description = QTextEdit()
        self.health_description.setPlaceholderText("For example: I have been diagnosed with type 2 diabetes and have been experiencing frequent headaches...")

        # Button layout
        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        next_button = QPushButton("Get Recommendations")
        next_button.clicked.connect(self.process_health_info)

        button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)

        # Add all to main layout
        layout.addWidget(header_label, 0, Qt.AlignCenter)
        layout.addLayout(form_layout)
        layout.addWidget(description_label)
        layout.addWidget(self.health_description)
        layout.addLayout(button_layout)

        details_widget.setLayout(layout)
        self.stacked_widget.addWidget(details_widget)

    def create_recommendations_page(self):
        recommendations_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Your Nutritional Recommendations")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        # Identified conditions
        self.conditions_label = QLabel("Based on your input, we've identified:")
        self.conditions_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        # Recommendations
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)

        # Disclaimer
        disclaimer_label = QLabel("Disclaimer: These recommendations are general advice and not a substitute for professional medical consultation.")
        disclaimer_label.setStyleSheet("font-style: italic; color: gray;")
        disclaimer_label.setWordWrap(True)

        # Buttons
        button_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.satisfaction_button = QPushButton("I'm Satisfied with These Recommendations")
        self.satisfaction_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.appointment_button = QPushButton("I Need to Consult a Doctor")
        self.appointment_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        button_layout.addWidget(back_button)
        button_layout.addWidget(self.satisfaction_button)
        button_layout.addWidget(self.appointment_button)

        # Add all to main layout
        layout.addWidget(header_label, 0, Qt.AlignCenter)
        layout.addWidget(self.conditions_label)
        layout.addWidget(self.recommendations_text)
        layout.addWidget(disclaimer_label)
        layout.addLayout(button_layout)

        recommendations_widget.setLayout(layout)
        self.stacked_widget.addWidget(recommendations_widget)

    def create_appointment_page(self):
        appointment_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Book an Appointment")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        # Form for appointment
        form_layout = QFormLayout()

        # Name input with validation (no empty field, only letters, spaces, and hyphens)
        self.name_input = QLineEdit()
        name_regex = QRegExp("^[A-Za-z\\s\\-']+$")
        name_validator = QRegExpValidator(name_regex)
        self.name_input.setValidator(name_validator)
        form_layout.addRow("Full Name*:", self.name_input)

        # Phone input with placeholder but we'll do custom validation
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Example: +91 9876543210 or 9876543210")
        form_layout.addRow("Phone Number*:", self.phone_input)

        # Email input with basic email validation
        self.email_input = QLineEdit()
        email_regex = QRegExp("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
        email_validator = QRegExpValidator(email_regex)
        self.email_input.setValidator(email_validator)
        form_layout.addRow("Email*:", self.email_input)

        specialist_label = QLabel("Select Specialist:")
        self.specialist_combo = QComboBox()
        self.specialist_combo.addItems(["General Practitioner", "Nutritionist", "Dietitian", "Endocrinologist", 
                                        "Gastroenterologist", "Cardiologist", "Rheumatologist"])
        form_layout.addRow(specialist_label, self.specialist_combo)

        date_label = QLabel("Select Date:")
        self.calendar = QCalendarWidget()
        # Set minimum date to today to prevent booking in the past
        self.calendar.setMinimumDate(QDate.currentDate())
        form_layout.addRow(date_label, self.calendar)

        time_label = QLabel("Select Time:")
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(9, 0))
        # Set time range for business hours (9 AM to 5 PM)
        self.time_edit.setTimeRange(QTime(9, 0), QTime(17, 0))
        form_layout.addRow(time_label, self.time_edit)

        # Required fields note
        required_fields_label = QLabel("* Required fields")
        required_fields_label.setStyleSheet("font-style: italic; color: gray;")

        # Buttons
        button_layout = QHBoxLayout()

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        book_button = QPushButton("Book Appointment")
        book_button.clicked.connect(self.book_appointment)

        button_layout.addWidget(back_button)
        button_layout.addWidget(book_button)

        # Add to main layout
        layout.addWidget(header_label, 0, Qt.AlignCenter)
        layout.addLayout(form_layout)
        layout.addWidget(required_fields_label)
        layout.addLayout(button_layout)

        appointment_widget.setLayout(layout)
        self.stacked_widget.addWidget(appointment_widget)

    def create_confirmation_page(self):
        confirmation_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Appointment Confirmed")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")

        # Confirmation details
        self.confirmation_text = QTextEdit()
        self.confirmation_text.setReadOnly(True)

        # Return button
        return_button = QPushButton("Return to Start")
        return_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Add to layout
        layout.addWidget(header_label, 0, Qt.AlignCenter)
        layout.addWidget(self.confirmation_text)
        layout.addWidget(return_button, 0, Qt.AlignCenter)

        confirmation_widget.setLayout(layout)
        self.stacked_widget.addWidget(confirmation_widget)

    def create_view_appointments_page(self):
        """Create a page to view all booked appointments."""
        view_appointments_widget = QWidget()
        layout = QVBoxLayout()

        # Header
        header_label = QLabel("Booked Appointments")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header_label, 0, Qt.AlignCenter)

        # Appointments list
        self.appointments_text = QTextEdit()
        self.appointments_text.setReadOnly(True)
        layout.addWidget(self.appointments_text)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, 0, Qt.AlignCenter)

        view_appointments_widget.setLayout(layout)
        self.stacked_widget.addWidget(view_appointments_widget)

    def validate_health_details(self):
        """Validate health details inputs and return True if valid."""
        # Validate age if provided (not mandatory)
        if self.age_input.text() and not self.age_input.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid age between 1 and 120.")
            return False

        # Validate gender selection
        if self.gender_input.currentIndex() == 0:  # "Select Gender" option
            QMessageBox.warning(self, "Missing Information", "Please select a gender option.")
            return False

        # Validate height if provided (not mandatory)
        if self.height_input.text() and not self.height_input.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid height between 50 and 250 cm.")
            return False

        # Validate weight if provided (not mandatory)
        if self.weight_input.text() and not self.weight_input.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid weight between 2 and 500 kg.")
            return False

        return True

    def is_valid_phone_number(self, phone):
        """Validates Indian phone number format."""
        # Remove all non-digit characters first
        digits_only = re.sub(r'\D', '', phone)
        
        # Check for Indian mobile number format
        # Option 1: +91 followed by 10 digits starting with 6-9
        # Option 2: 0 followed by 10 digits starting with 6-9
        # Option 3: Just 10 digits starting with 6-9
        
        if len(digits_only) == 10:
            # Just 10 digits
            return digits_only[0] in '6789'
        elif len(digits_only) == 11 and digits_only[0] == '0':
            # 0 followed by 10 digits
            return digits_only[1] in '6789'
        elif len(digits_only) == 12 and digits_only[0:2] == '91':
            # 91 followed by 10 digits
            return digits_only[2] in '6789'
        elif len(digits_only) == 13 and digits_only[0:3] == '091':
            # 091 followed by 10 digits
            return digits_only[3] in '6789'
        
        return False

    def process_health_info(self):
        """Process health information using the backend after validation."""
        # First validate the inputs
        if not self.validate_health_details():
            return

        health_description = self.health_description.toPlainText().strip()
        if not health_description:
            QMessageBox.warning(self, "Missing Information", "Please describe your health concerns.")
            return

        print("Calling backend to process health info...")  # Debugging statement
        conditions_text, recommendations = self.backend.process_health_info(health_description)
        print("Backend processing complete.")  # Debugging statement

        self.conditions_label.setText(conditions_text)
        self.recommendations_text.setText(recommendations)
        self.stacked_widget.setCurrentIndex(2)

    def validate_appointment_details(self):
        """Validate appointment form inputs and return True if valid."""
        # Check that name is provided and valid
        if not self.name_input.text() or not self.name_input.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid name (letters, spaces, and hyphens only).")
            return False

        # Check phone number with our custom validation
        phone = self.phone_input.text().strip()
        if not phone or not self.is_valid_phone_number(phone):
            QMessageBox.warning(self, "Invalid Phone Number", 
                              "Please enter a valid Indian mobile number.\n"
                              "Examples: +91 9876543210, 09876543210, 9876543210")
            return False

        # Check that email is provided and valid
        if not self.email_input.text() or not self.email_input.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid email address.")
            return False

        # Validate selected date (ensure it's not in the past)
        selected_date = self.calendar.selectedDate()
        if selected_date < QDate.currentDate():
            QMessageBox.warning(self, "Invalid Date", "Please select a date in the future.")
            return False

        return True

    def book_appointment(self):
        """Book an appointment and save the data using the backend after validation."""
        if not self.validate_appointment_details():
            return

        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        specialist = self.specialist_combo.currentText()
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        time = self.time_edit.time().toString("HH:mm")

        # Call the backend to book the appointment and save data
        confirmation_message = self.backend.book_appointment(name, phone, email, specialist, date, time)
        self.confirmation_text.setText(confirmation_message)
        self.stacked_widget.setCurrentIndex(4)

    def load_appointments(self):
        """Load and display booked appointments."""
        appointments = self.backend.load_appointment_data()
        if not appointments:
            self.appointments_text.setText("No appointments found.")
            return

        appointments_text = "Booked Appointments:\n\n"
        for appointment in appointments:
            appointments_text += (
                f"Name: {appointment['name']}\n"
                f"Phone: {appointment['phone']}\n"
                f"Email: {appointment['email']}\n"
                f"Specialist: {appointment['specialist']}\n"
                f"Date: {appointment['date']}\n"
                f"Time: {appointment['time']}\n"
                f"{'-' * 30}\n"
            )
        self.appointments_text.setText(appointments_text)

if __name__ == "__main__":
    app = QApplication([])
    kiosk = HealthConsultationKioskUI()  # Changed instantiation
    kiosk.show()
    app.exec_()