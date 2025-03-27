import sys
import os
import uuid  # For auto-generating UID

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from Interface.modules.Meal_day import MealDay  # Ensure correct class name
except ImportError as e:
    print(f"❌ Error importing Meal_day: {e}")

try:
    from Interface.ui.meal_day_ui import MealPlanForDayUI  
except ImportError as e:
    print(f"❌ Error importing MealPlanForDayUI: {e}")

# Ensure Python finds the correct modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui')))

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton,
    QGridLayout, QHBoxLayout, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MealRecommendationUI(QWidget):  
    def __init__(self, kiosk=None):
        try:
            super().__init__()
            self.kiosk = kiosk  # Store reference to kiosk UI
            print("🔹 MealRecommendationUI: Initializing...")  

            self.setWindowTitle("Meal Recommendation")
            self.initUI()
            print("✅ MealRecommendationUI: UI setup completed successfully!")
        
        except Exception as e:
            print(f"❌ Error in MealRecommendationUI __init__: {e}")

    def initUI(self):
        print("🔹 Setting up UI for MealRecommendationUI")  
        self.setWindowTitle("Personalized Meal Recommendation")
        self.setGeometry(200, 100, 1133, 731)
        self.setStyleSheet("background-color: #f0f8ff; padding: 15px;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # Header
        header_label = QLabel("🍽 Personalized Meal Suggestion")
        header_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Grid Layout for form fields
        form_layout = QGridLayout()
        form_layout.setSpacing(15)

        # User Input Fields
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.bmi_input = QLineEdit()
        
        self.bmi_category_combo = QComboBox()
        self.bmi_category_combo.addItems(["Underweight", "Normal", "Overweight", "Obese"])

        self.dietary_combo = QComboBox()
        self.dietary_combo.addItems(["Vegetarian", "Vegan", "Keto", "Paleo", "No Restriction"])

        self.meal_type_combo = QComboBox()
        self.meal_type_combo.addItems(["Daily", "Weekly", "Breakfast", "Lunch", "Dinner"])

        self.uid_input = QLineEdit(str(uuid.uuid4()))  # Generate UID
        self.uid_input.setReadOnly(True)  # Prevent editing

        self.health_goal_input = QLineEdit()
        self.allergy_input = QLineEdit()

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])

        self.activity_level_combo = QComboBox()
        self.activity_level_combo.addItems(["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

        self.occupation_combo = QComboBox()
        self.occupation_combo.addItems(["Student", "Office Worker", "Athlete", "Retired", "Other"])

        # Adding Widgets to Grid Layout
        def add_form_row(label, widget, row, col):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            form_layout.addWidget(lbl, row, col)
            form_layout.addWidget(widget, row, col + 1)

        add_form_row("Name:", self.name_input, 0, 0)
        add_form_row("Age:", self.age_input, 1, 0)
        add_form_row("BMI Value:", self.bmi_input, 2, 0)
        add_form_row("BMI Category:", self.bmi_category_combo, 3, 0)
        add_form_row("Dietary Preference:", self.dietary_combo, 4, 0)
        add_form_row("Meal Type:", self.meal_type_combo, 5, 0)

        add_form_row("UID:", self.uid_input, 0, 2)
        add_form_row("Health Goal:", self.health_goal_input, 1, 2)
        add_form_row("Allergies:", self.allergy_input, 2, 2)
        add_form_row("Gender:", self.gender_combo, 3, 2)
        add_form_row("Activity Level:", self.activity_level_combo, 4, 2)
        add_form_row("Occupation:", self.occupation_combo, 5, 2)

        main_layout.addLayout(form_layout)

        # Buttons
        self.mealPlanForDay = QPushButton("Get Meal Plan for Day")
        self.mealPlanForWeek = QPushButton("Customize Meal for Week")
        self.backToKiosk = QPushButton("Back to Kiosk")

        button_style = """
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
        """
        self.mealPlanForDay.setStyleSheet(button_style)
        self.mealPlanForWeek.setStyleSheet(button_style)
        self.backToKiosk.setStyleSheet(button_style)

        # Connect Buttons
        self.mealPlanForDay.clicked.connect(self.get_meal_plan_for_day)
        self.mealPlanForWeek.clicked.connect(self.customize_meal_for_week)
        self.backToKiosk.clicked.connect(self.return_to_kiosk)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.mealPlanForDay)
        button_layout.addWidget(self.mealPlanForWeek)
        button_layout.addWidget(self.backToKiosk)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        print("✅ UI setup completed for MealRecommendationUI")

    def return_to_kiosk(self):
        print("🔄 Returning to Kiosk UI...")

        if self.kiosk:  
            self.hide()  # Hide meal recommendation UI before switching
            self.kiosk.show()  # Bring the Kiosk UI to the front
        else:
            print("⚠️ Warning: Kiosk UI is not set!")

    def validate_inputs(self):
        """Validate user inputs before proceeding."""
        if not self.name_input.text().strip():
            print("⚠️ Name cannot be empty!")
            return False
        if not self.age_input.text().isdigit():
            print("⚠️ Age must be a number!")
            return False
        try:
            float(self.bmi_input.text())  # Ensure BMI is a valid number
        except ValueError:
            print("⚠️ BMI must be a numeric value!")
            return False
        return True

    def get_meal_plan_for_day(self):
        """Generate meal plan for the day and display it in the UI."""
        if not self.validate_inputs():
            return

        print("🍽 Generating daily meal plan...")

        try:
            # Extract user inputs
            user_data = {
                "name": self.name_input.text().strip(),
                "age": int(self.age_input.text().strip()),
                "bmi": float(self.bmi_input.text().strip()),
                "bmi_category": self.bmi_category_combo.currentText(),  # ✅ CORRECT KEY
                "dietary_preference": self.dietary_combo.currentText(),
                "meal_type": self.meal_type_combo.currentText(),
                "health_goal": self.health_goal_input.text().strip(),
                "allergies": self.allergy_input.text().strip(),
                "gender": self.gender_combo.currentText(),
                "activity_level": self.activity_level_combo.currentText(),
                "occupation": self.occupation_combo.currentText(),
            }

            print(f"User data: {user_data}")  # Debugging print

            meal_day = MealDay(user_data)
            meal_plan = meal_day.meal_plan_for_day()

        # Handle backend error messages
            if isinstance(meal_plan, dict) and "message" in meal_plan:
                meal_plan = meal_plan["message"]  # Extract error message

        # Ensure meal_plan is a string
            self.meal_plan_ui = MealPlanForDayUI(str(meal_plan))
            self.meal_plan_ui.show()

        except Exception as e:
            print(f"❌ Error: {str(e)}")
        # Show error to user
        self.meal_plan_ui = MealPlanForDayUI(f"Error: {str(e)}")
        self.meal_plan_ui.show()

    def customize_meal_for_week(self):
        """Customize meal plan for the week."""
        if not self.validate_inputs():
            return
        print("📅 Customizing weekly meal plan...")
        # Call backend logic here for customizing weekly meal plan

# Run standalone test
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        kiosk_window = QWidget()  # Placeholder for the kiosk UI
        kiosk_window.setWindowTitle("Kiosk UI")
        kiosk_window.setGeometry(200, 100, 800, 600)

        window = MealRecommendationUI(kiosk=kiosk_window)  # Pass kiosk reference
        kiosk_window.show()  # Show kiosk UI first
        window.show()  # Then show meal recommendation UI
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ Error launching MealRecommendationUI: {e}")