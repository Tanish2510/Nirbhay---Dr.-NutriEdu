import random
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal

# Global variable to store the thread instance
tts_thread = None  

def get_response(query):
    """Returns a chatbot response for a given food query."""
    food_data = {
        "apple": "An apple has about 95 calories, 25g of carbohydrates, and is rich in fiber.",
        "banana": "A banana contains about 105 calories, 27g of carbohydrates, and is a good source of potassium.",
        "carrot": "Carrots are low in calories (41 per 100g) and high in vitamin A, which is great for vision.",
        "milk": "One cup of milk provides about 103 calories, 8g of protein, and is rich in calcium.",
        "egg": "One egg contains about 70 calories, 6g of protein, and healthy fats."
    }
    
    query = query.lower()
    response = food_data.get(query, None)
    
    if response:
        return response
    else:
        fallback_responses = [
            f"Sorry, I don't have information on '{query}'. Try another food item!",
            "I am still learning! Could you ask about another food?",
            f"I'm not sure about '{query}', but I can help with other foods!"
        ]
        return random.choice(fallback_responses)

def voice_input():
    """Captures user's voice input and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        try:
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."


class TextToSpeechThread(QThread):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(self.text)
        engine.runAndWait()
        self.finished.emit()

def speak(text):
    """Plays text-to-speech for chatbot responses asynchronously."""
    global tts_thread  # Use the global variable

    if tts_thread and tts_thread.isRunning():
        tts_thread.quit()  
        tts_thread.wait()  

    tts_thread = TextToSpeechThread(text)
    tts_thread.finished.connect(clean_thread)  
    tts_thread.start()

def clean_thread():
    """Cleans up the thread after it finishes execution."""
    global tts_thread  
    tts_thread = None  # Reset the thread after finishing
