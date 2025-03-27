import sys
import threading
from PyQt5 import QtWidgets
from Interface.ui.Kiosk_ui import Ui_MainWindow
from Interface.ui.bmi_ui import BMICalculatorUI
from Interface.ui.nutrition_ui import NutritionChatbot
from Interface.ui.Meal_ui import MealRecommendationUI
from Interface.modules.video_handler import VideoHandler  # Import Video Module
from Interface.modules.audio_handler import AudioHandler  # Import Audio Module
from Interface.ui.Bookconsultation_ui import NutritionKioskUI  # Uncomment this line
from Interface.ui.patient_history_ui import PatientInfoDialog  # Add this line
from Commantips_ui import HealthConsultationKioskUI
# from Interface.modules.Bookconsultation import NutritionKioskApp  # You might not need this import
# from Interface.ui.Bookconsultation_ui import NutritionKioskUI  # Add this import
# from Interface.modules.Bookconsultation import NutritionKioskApp  # Add this import

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing MainApp")
        self.setupUi(self)
        print("Kiosk UI setup completed")

        # Ensure video widget exists
        if hasattr(self, "video_widget"):
            self.video_handler = VideoHandler(self.video_widget)  # Use VideoHandler
            self.video_handler.load_video()
        else:
            print("Error: video_widget not found in Kiosk_ui.py")
            return

        # Connect buttons to functions
        self.connect_buttons()

        # Store UI references
        self.bmi_window = None  
        self.nutrition_window = None  
        self.meal_window = None
        self.consultation_window = None  # Add this line

        # Start speech in a separate thread
        self.audio_handler = AudioHandler()  # Use AudioHandler
        self.start_speech_thread("Welcome to the AI Health Kiosk. This is your guide to a healthy lifestyle. "
                                "Here, you can get nutritional advice, and plan your meals.")

    def start_speech_thread(self, text):
        """Start speech in a separate thread."""
        speech_thread = threading.Thread(target=self.audio_handler.start_speech, args=(text,))
        speech_thread.daemon = True  # Daemonize thread to exit when the main program exits
        speech_thread.start()

    def connect_buttons(self):
        """Connects buttons to their respective functions."""
        button_map = {
            "pushBtnCalculateBMI": self.open_bmi_calculator,
            "pushBtnNutrition": self.open_nutrition_chatbot,
            "pushBtnMeal": self.open_meal_recommendation,
            "pushBtnAppoinment": self.open_consultation_window, # Add this line
            "pushBtnHealthConsult": self.open_health_consultation,  # Use the EXACT name from Kiosk_ui.py
            "pushBtnDiscuss": self.open_patient_history
        }

        for btn_name, method in button_map.items():
            if hasattr(self, btn_name):
                getattr(self, btn_name).clicked.connect(method)
            else:
                print(f"Error: {btn_name} not found in Kiosk_ui.py")

    def open_bmi_calculator(self):
        """Opens the BMI Calculator window."""
        if not self.bmi_window or not self.bmi_window.isVisible():
            self.bmi_window = BMICalculatorUI(self)
            self.bmi_window.show()
            self.hide()
            self.bmi_window.destroyed.connect(self.show_kiosk)

    def open_nutrition_chatbot(self):
        """Opens the Nutrition Chatbot window."""
        if not self.nutrition_window or not self.nutrition_window.isVisible():
            self.nutrition_window = NutritionChatbot(self)
            self.nutrition_window.show()
            self.hide()
            self.nutrition_window.destroyed.connect(self.show_kiosk)

    def open_meal_recommendation(self):
        """Opens the Meal Recommendation UI."""
        if not self.meal_window or not self.meal_window.isVisible():
            self.meal_window = MealRecommendationUI(self)
            self.meal_window.show()
            self.hide()
            self.meal_window.destroyed.connect(self.show_kiosk)

    def open_consultation_window(self):
        if not self.consultation_window or not self.consultation_window.isVisible():
            self.consultation_window = NutritionKioskUI()  # <-- CORRECT CLASS NAME
            self.consultation_window.show()
            self.hide()
            self.consultation_window.destroyed.connect(self.show_kiosk)
    
    def open_health_consultation(self):
        """Opens the Health Consultation window."""
        if not hasattr(self, 'health_consult_window') or not self.health_consult_window.isVisible():
            self.health_consult_window = HealthConsultationKioskUI(parent=self)
            self.health_consult_window.show()
            self.hide()
            self.health_consult_window.destroyed.connect(self.show_kiosk)

    def open_patient_history(self):
        """Opens the Patient History dialog."""
        if not hasattr(self, 'patient_history_window') or not self.patient_history_window:
            self.patient_history_window = PatientInfoDialog()
            self.patient_history_window.show()
            self.hide()
            self.patient_history_window.destroyed.connect(self.show_kiosk)

    def show_kiosk(self):
        """Show the Kiosk again when any window is closed."""
        self.show()
        self.bmi_window = None
        self.nutrition_window = None
        self.meal_window = None
        self.consultation_window = None  # Add this line
        self.health_consult_window = None
        self.patient_history_window = None

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())