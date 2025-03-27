import pyttsx3
import time
import threading

class AudioHandler:
    def __init__(self):
        """Initializes the text-to-speech engine."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Default speech rate
            self.engine.setProperty('volume', 1.0)  # Default volume
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            self.engine = None

    def speak(self, text):
        """Plays text-to-speech."""
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Error during speech: {e}")
        else:
            print("TTS engine not initialized.")

    def start_speech(self, text, callback=None):
        """Starts speech in a separate thread and calls a callback when done."""
        if self.engine:
            threading.Thread(target=self._speak_with_callback, args=(text, callback), daemon=True).start()
        else:
            print("TTS engine not initialized.")

    def _speak_with_callback(self, text, callback):
        """Plays speech and calls the callback when done."""
        self.speak(text)
        if callback:
            callback()