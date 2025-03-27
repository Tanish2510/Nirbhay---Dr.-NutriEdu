import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QApplication, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MealPlanForDayUI(QWidget):
    def __init__(self, meal_plan):
        super().__init__()
        self.meal_plan = meal_plan  # The formatted meal plan passed from the Meal_day.py module
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Meal Plan for Today")
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f8ff; padding: 15px;")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        header_label = QLabel("🍽 Meal Plan for Today")
        header_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Scroll area for meal details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Store this label as an instance variable to update it later
        self.meal_plan_text_label = QLabel(self.meal_plan)
        self.meal_plan_text_label.setFont(QFont("Arial", 14))
        self.meal_plan_text_label.setAlignment(Qt.AlignLeft)
        self.meal_plan_text_label.setWordWrap(True)
        scroll_layout.addWidget(self.meal_plan_text_label)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Close Button
        close_button = QPushButton("Close")
        close_button.setStyleSheet(""" 
            QPushButton {
                background-color: #008CBA;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005f73;
            }
        """)
        close_button.clicked.connect(self.close_application)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def close_application(self):
        """Close the application."""
        self.close()

# Example Usage (Main Application Code)
if __name__ == "__main__":
    from Meal_day import MealDay  # Import the MealDay class

    app = QApplication(sys.argv)

    # Example user data (this should ideally come from user input)
    user_data = {
        "age": 30,
        "gender": "female",
        "activity_level": "moderate",
        "bmi": "normal",
        "health_goal": "weight_loss",
        "dietary_preference": "vegetarian",
        "allergies": ["nuts"]
    }

    # Create an instance of MealDay and get the meal plan for today
    meal_day = MealDay(user_data)
    formatted_meal_plan = meal_day.meal_plan_for_day()  # Get formatted meal plan

    # Instantiate MealPlanForDayUI with the formatted meal plan
    meal_plan_ui = MealPlanForDayUI(meal_plan=formatted_meal_plan)

    # Show the Meal Plan UI
    meal_plan_ui.show()

    sys.exit(app.exec_())


