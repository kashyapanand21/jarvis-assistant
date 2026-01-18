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

recognizer = sr.Recognizer() # to recognize voice
engine = pyttsx3.init() # to initialize the ttsx engine
newsapi = "73a662d2c64041e6b976111613884e71"

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def speak(text):
#     engine = pyttsx3.init()   
#     engine.say(text)
#     engine.runAndWait()


def speak(text):
    print(f"[Speaking]: {text}")
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
        
        # Generate speech
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file)
        
        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        
        # Clean up
        os.unlink(temp_file)
        time.sleep(0.3)
        
    except Exception as e:
        print(f"TTS Error: {e}")


def googleProcess(command: str) -> str:
    client = genai.Client(api_key="AIzaSyAxXoj8cYx_yYb0-AktHUpQs0cUlZedAmQ")

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
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        # the split will convert it into a list
        link = musicLibrary.music(song)
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
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
    
    jarvis_active = False  # ← NEW: Track if Jarvis is in active listening mode
    
    while True:
        #! Listen for the wake word "Jarvis"

        # obtain audio from the microphone
        # r = sr.Recognizer()
        
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                if not jarvis_active:
                    print("Listening for wake word 'hello'...")  # ← NEW
                else:
                    print("Jarvis Active - Listening for command...")  # ← NEW
                
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            print(f"Recognized: {word}")  # ← Changed to show what was recognized

            # Check if wake word is spoken
            if word.lower() == "hello":
                if not jarvis_active:
                    # Activate Jarvis
                    jarvis_active = True
                    speak("Yes, I'm listening")
                else:
                    # Reset/restart Jarvis
                    jarvis_active = False
                    speak("Restarting")
                    time.sleep(0.5)
                    jarvis_active = True
                    speak("Yes, I'm listening")

            # If Jarvis is active and it's not the wake word, process as command
            elif jarvis_active:
                processCommand(word)
        
            # with sr.Microphone() as source:
            #     recognizer.adjust_for_ambient_noise(source, duration=1.2)
            #     print("Listening for wake word...")
            #     audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            # wake = recognizer.recognize_google(audio).lower()
            # print("Heard:", wake)

            # if wake == "namaste":
            #     speak("Yaa...")  # This will run reliably now
            #     with sr.Microphone() as source:
            #         recognizer.adjust_for_ambient_noise(source, duration=1)
            #         print("Assistant Active...")
            #         audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

            #         cmd = recognizer.recognize_google(audio)
            #         print("Command:", cmd)
            #         processCommand(cmd)



        except sr.WaitTimeoutError:
            # Timeout - continue listening
            continue
        except sr.UnknownValueError:
            # Could not understand audio
            if jarvis_active:
                print("Could not understand, please repeat")
            continue
        except Exception as e:
            print(f"Error: {e}")