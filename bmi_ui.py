from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from modules.bmi import BMICalculator


class BMICalculatorUI(QWidget):
    def __init__(self, kiosk):
        super().__init__()
        self.kiosk = kiosk  # Store reference to kiosk window
        self.bmi_calculator = BMICalculator()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Smart BMI Chatbot")
        self.setGeometry(200, 100, 1133, 731)
        self.setStyleSheet("background-color: #f5f5f5;")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Title Label
        self.title_label = QLabel("🤖 Smart BMI Chatbot")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 14))
        self.chat_display.setStyleSheet("""
            background-color: white;
            border: 2px solid #007BFF;
            border-radius: 10px;
            padding: 10px;
            min-height: 400px;
        """)
        layout.addWidget(self.chat_display)

        # Buttons
        self.weight_button = self.create_button("⚖️ Speak Weight", "#007BFF", self.speak_weight)
        layout.addWidget(self.weight_button)

        self.height_button = self.create_button("📏 Speak Height", "#17A2B8", self.speak_height)
        layout.addWidget(self.height_button)

        self.bmi_button = self.create_button("📊 Calculate BMI", "#FFC107", self.calculate_bmi)
        layout.addWidget(self.bmi_button)

        self.book_button = self.create_button("📅 Book Consultation", "#28a745", self.book_consultation)
        layout.addWidget(self.book_button)

        # Back to Kiosk Button
        self.close_button = self.create_button("🔙 Back to Kiosk", "#dc3545", self.go_back_to_kiosk)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def create_button(self, text, color, handler):
        """Helper method to create styled buttons."""
        button = QPushButton(text)
        button.setFont(QFont("Arial", 14, QFont.Bold))
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 12px; border-radius: 10px;")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(handler)
        return button

    def speak_weight(self):
        """Trigger speech recognition for weight input."""
        self.bmi_calculator.get_weight(self.update_chat, self.update_chat)

    def speak_height(self):
        """Trigger speech recognition for height input."""
        self.bmi_calculator.get_height(self.update_chat, self.update_chat)

    def calculate_bmi(self):
        """Calculate BMI and display result."""
        self.bmi_calculator.calculate_bmi(self.update_chat)

    def book_consultation(self):
        """Placeholder function for booking a consultation."""
        self.update_chat("User: Booked a Consultation")

    def go_back_to_kiosk(self):
        """Close BMI Chatbot and show Kiosk again."""
        self.kiosk.show()
        self.close()

    def update_chat(self, message):
        """Update chat display with messages."""
        self.chat_display.append(message)
