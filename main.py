import time
import speech_recognition as sr
import webbrowser 
import pyttsx3 
import musicLibrary
import requests
from google import genai
from gtts import gTTS
import pygame
import os
import tempfile


# Initialize Pygame Mixer globally to reduce latency
pygame.mixer.init()

# Secure API Keys from Environment Variables
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")

recognizer = sr.Recognizer() # to recognize voice
engine = pyttsx3.init() # to initialize the ttsx engine


# def speak(text):
#     engine.say(text)
#     engine.runAndWait()


def speak(text):
    print(f"[Speaking]: {text}")
    temp_file = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
        
        # Generate speech
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file)
        
        # Play audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Release the file lock so it can be deleted
        pygame.mixer.music.unload()
        
    except Exception as e:
        print(f"TTS Error: {e}")
        
    finally:
        # Clean up
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except PermissionError:
                pass # Handled by OS later or restart




def googleProcess(command: str) -> str:
    if not GENAI_API_KEY:
        return "Gemini API Key not found."
    client = genai.Client(api_key=GENAI_API_KEY)

    prompt = f"""
    You are Jarvis, a helpful virtual assistant.
    User said: {command}
    Respond briefly and in plain sentences (no markdown).
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text  
   

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play "):
        parts = c.lower().split(" ", 1)
        if len(parts) > 1:
            song = parts[1]
            try:
                link = musicLibrary.music(song)
                webbrowser.open(link)
            except Exception as e:
                print(f"Music Error: {e}")
                speak("I couldn't find that song.")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            # it parse the JSON response
            data = r.json()

            #It extracts the articles 
            articles = data.get('articles', [])

            #It prints the headlines 
            for article in articles:
                speak(article['title']) 
    else:
        output = googleProcess(c)
        speak(output)
        print(output)
        time.sleep(1)
        


if __name__ == "__main__":
    speak("Initializing Jarvis")
    
    orion_active = False  #if Jarvis is in active listening mode
    
    while True:
        #! Listen for the wake word "Jarvis"

        # obtain audio from the microphone
        # r = sr.Recognizer()
        
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                if not orion_active:
                    print("Listening for wake word 'Jarvis'...")  
                else:
                    print("Jarvis Active - Listening for command...")  
                
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            print(f"Recognized: {word}")  

            # Check if wake word is spoken
            # Strip punctuation and whitespace for robust detection
            word_clean = word.lower().strip(".,!? ")
            if word_clean == "jarvis":
                if not orion_active:
                    # Activate jarvis
                    orion_active = True
                    speak("Yes, I'm listening")
                else:
                    # Reset/restart jarvis
                    orion_active = False
                    speak("Restarting")
                    time.sleep(0.5)
                    orion_active = True
                    speak("Yes, I'm listening")

            # If jarvis is active and it's not the wake word, process as command
            elif orion_active:
                processCommand(word)
                
        except sr.WaitTimeoutError:
            # Timeout - continue listening
            continue
        except sr.UnknownValueError:
            # Could not understand audio
            if orion_active:
                print("Could not understand, please repeat")
            continue
        except Exception as e:
            print(f"Error: {e}")