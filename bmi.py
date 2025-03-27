from PyQt5.QtCore import QThread, pyqtSignal
import speech_recognition as sr
import pyttsx3
import re
from PyQt5.QtCore import Qt

class VoiceInputThread(QThread):
    result_signal = pyqtSignal(str)  # Signal to send recognized text
    error_signal = pyqtSignal(str)   # Signal for errors

    def __init__(self, prompt, voice_id=0, rate=160):
        super().__init__()
        self.prompt = prompt
        self.voice_id = voice_id  # Select Male/Female voice
        self.rate = rate  # Speed of speech
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.configure_speech_engine()

    def configure_speech_engine(self):
        """Configure pyttsx3 voice settings."""
        voices = self.engine.getProperty("voices")
        if self.voice_id < len(voices):
            self.engine.setProperty("voice", voices[self.voice_id].id)
        self.engine.setProperty("rate", self.rate)  # Adjust speaking speed

    def speak(self, text):
        """Convert text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()

    def run(self):
        """Capture user input via voice."""
        mic = sr.Microphone()
    
        # Speak prompt BEFORE activating the mic
        self.speak(self.prompt)

        with mic as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                self.error_signal.emit("⏳ Timeout! Please try again.")
                return

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            self.result_signal.emit(text)
        except sr.UnknownValueError:
            self.error_signal.emit("🤖 I didn't understand. Please try again.")
        except sr.RequestError:
            self.error_signal.emit("⚠️ Speech recognition service error.")

class BMICalculator:
    def __init__(self):
        self.weight = None
        self.height = None

    def get_weight(self, callback, error_callback):
        """Trigger voice input for weight."""
        self.voice_thread = VoiceInputThread("Please say your weight in kilograms.")
        self.voice_thread.result_signal.connect(
            lambda text: self.set_weight(text, callback), type=Qt.QueuedConnection
      )  
        self.voice_thread.error_signal.connect(error_callback, type=Qt.QueuedConnection)
        self.voice_thread.start()

    def get_height(self, callback, error_callback):
        """Trigger voice input for height."""
        self.voice_thread = VoiceInputThread("Please say your height in centimeters.")
        self.voice_thread.result_signal.connect(
            lambda text: self.set_height(text, callback), type=Qt.QueuedConnection
        ) 
        self.voice_thread.error_signal.connect(error_callback, type=Qt.QueuedConnection)
        self.voice_thread.start()
    
    def set_weight(self, text, callback):
        """Extract and store weight from voice input."""
        print(f"DEBUG: Recognized weight -> {text}")  # Debugging log

        weight = self.extract_number(text)  # Extract numerical value

        if weight is not None:
            self.weight = weight
            callback(f"✅ Weight: {self.weight} kg")
        else:
            callback("⚠️ Invalid weight input. Please try again.")

    def set_height(self, text, callback):
        """Extract and store height from voice input."""
        print(f"DEBUG: Recognized height -> {text}")  # Debugging log

        height = self.extract_number(text)  # Extract numerical value

        if height is not None:
            self.height = height
            callback(f"✅ Height: {self.height} cm")
        else:
            callback("⚠️ Invalid height input. Please try again.")

    def extract_number(self, text):
        """Extract first valid number from the recognized text."""
        match = re.search(r"\d+(\.\d+)?", text)  # Find numbers like 70 or 70.5
        return float(match.group()) if match else None

    def calculate_bmi(self, callback):
        """Calculate and display BMI based on user input."""
        if self.weight is None or self.height is None:
            callback("⚠️ Please enter both weight and height first.")
            return

        height_m = self.height / 100  # Convert cm to meters
        bmi = self.weight / (height_m ** 2)  # BMI formula
        category = self.get_bmi_category(bmi)

        result_text = f"📊 Your BMI is **{bmi:.2f}** ({category})"
        callback(result_text)

    def get_bmi_category(self, bmi):
        """Determine BMI category based on WHO standards."""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"