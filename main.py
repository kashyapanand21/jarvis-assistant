import speech_recognition as sr
import webbrowser 
import pyttsx3 
import musicLibrary
import requests

recognizer = sr.Recognizer() # to recognize voice
engine = pyttsx3.init() # to initialize the ttsx engine
newsapi = "73a662d2c64041e6b976111613884e71"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startwith("play"):
        song = c.lower().split(" ")[1]
        # the split will convert it into a list
        link = musicLibrary.music(song)
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title']) 


        # data = r.json()

        # if data.get("status") != "ok":
        #     print("API error:", data)
        #     exit(1)

        # articles = data.get("articles", [])

        # if not articles:
        #     print("No headlines found.")
        # else:
        #     for i, article in enumerate(articles, 1):
        #         title = article.get("title")
        #         if title:
        #             print(f"{i}. {title}")

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
                speak("Yaa...")
                # Listen for word        
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    word = r.recognize_google(audio)

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



        except Exception as e:
            print("Error; {0}".format(e))