import speech_recognition as sr
import webbrowser 
import pyttsx3 

recognizer = sr.Recognizer() # to recognize voice
engine = pyttsx3.init() # to initialize the ttsx engine

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    print(c + " this is process command")
    pass    

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        #! Listen for the wake word "Jarvis"

        # obtain audio from the microphone
        r = sr.Recognizer()
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source , timeout = 2 , phrase_time_limit = 1)
            word = r.recognize_google(audio)
            print(word)
            if (word.lower()== "hello"): 
                speak("I am listening...")   
                # Listen for word        
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    word = r.recognize_google(audio)

                    processCommand(word)



        except Exception as e:
            print("Error; {0}".format(e))