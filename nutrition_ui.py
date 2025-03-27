from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser, QLineEdit,
    QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from nutrition import get_response, speak ,voice_input  # Moved logic to nutrition.py

class NutritionChatbot(QWidget):
    def __init__(self, kiosk):
        super().__init__()
        self.kiosk = kiosk
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🤖 Smart Nutrition Chatbot")
        self.setGeometry(200, 100, 1133, 731)
        self.setStyleSheet("background-color: #f0f8ff;")

        self.layout = QVBoxLayout()

    # Header Label
        self.header_label = QLabel("🍏 Nutritional Value Chatbot")
        self.header_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("color: #2E86C1;")
        self.layout.addWidget(self.header_label)

    # Chat Display
        self.chat_display = QTextBrowser(self)
        self.chat_display.setFont(QFont("Arial", 12))
        self.chat_display.setStyleSheet("""
            background-color: white;
            border: 2px solid #007BFF;
            border-radius: 10px;
            padding: 10px;
            min-height: 300px;
        """)
        self.layout.addWidget(self.chat_display)

    # Input Layout (Text + Button)
        input_layout = QHBoxLayout()

        self.input_box = QLineEdit(self)
        self.input_box.setFont(QFont("Arial", 12))
        self.input_box.setPlaceholderText("Type your query here...")
        self.input_box.setStyleSheet("""
            background-color: white;
            border: 2px solid #007BFF;
            border-radius: 5px;
            padding: 8px;
            color: #333;
        """)
        input_layout.addWidget(self.input_box)

        button_style = """
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005f7f;
            }
        """

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_button.setStyleSheet(button_style)
        self.send_button.clicked.connect(self.process_input)
        input_layout.addWidget(self.send_button)

        self.layout.addLayout(input_layout)

    # Speech Button
        self.speak_button = QPushButton("🎤 Speak Query", self)
        self.speak_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.speak_button.setStyleSheet(button_style)
        self.speak_button.clicked.connect(self.voice_input)
        self.layout.addWidget(self.speak_button)

    # Back to Kiosk Button
        self.back_button = QPushButton("⬅ Back to Kiosk", self)
        self.back_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.back_button.setStyleSheet("background-color: #ff5733; color: white; padding: 8px; border-radius: 5px;")
        self.back_button.clicked.connect(self.close_nutrition_chatbot)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    # Initial Bot Message
        self.chat_display.append("Chatbot: Hello! Ask me about a food item.")
        speak("Hello! Ask me about a food item.")  # Correct usage


    def process_input(self):
        """Handles user text input and displays chatbot response."""
        user_query = self.input_box.text().strip()
        if not user_query:
            return

        self.chat_display.append(f"You: {user_query}")

        # Get chatbot response
        bot_response = get_response(user_query)
        self.chat_display.append(f"Chatbot: {bot_response}")

        # Speak the response
        speak(bot_response)

        # Clear input box
        self.input_box.clear()


    def voice_input(self):
        """Handles voice input and processes the recognized text."""
        user_query = voice_input()
    
        if user_query.startswith("Sorry") or user_query.startswith("Speech recognition service"):
            self.chat_display.append(f"Chatbot: {user_query}")
        else:
            self.input_box.setText(user_query)
            self.process_input()  # Process the recognized voice input

    def close_nutrition_chatbot(self):
        """Closes Nutrition Chatbot and reopens the Kiosk."""
        self.close()  # Close the chatbot
        self.kiosk.show()  # Show the main kiosk window
