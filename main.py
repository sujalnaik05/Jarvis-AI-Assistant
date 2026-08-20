import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import ollama

recognizer = sr.Recognizer()
newsapi ="4e752eeff4c54785bc3bc93967a63a89"

def speak(text):
    print("Jarvis speaking:", text)

    engine = pyttsx3.init("sapi5")
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def ask_ollama(question):
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        options={
            "num_predict": 150
        }
    )

    return response["message"]["content"]

def processCommand(c):
    if "stop jarvis" in c.lower() or "exit jarvis" in c.lower():
        speak("Goodbye!")
        exit()

    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        print("Song searched:", song)
        print("Available songs:", musiclibrary.music.keys())

        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)

    elif "news" in c.lower():
        print("NEWS COMMAND DETECTED")

        r = requests.get(
    f"https://newsapi.org/v2/everything?q=India OR Indian&language=en&sortBy=publishedAt&apiKey={newsapi}"
)
        print("STATUS:", r.status_code)

        data = r.json()

        print("Total articles:", len(data.get("articles", [])))

        if len(data.get("articles", [])) == 0:
            speak("Sorry, I could not find any news right now.")
        else:
            speak("Here are the latest Indian news headlines.")

            for article in data["articles"][:5]:
                title = article["title"]
                print("Speaking:", title)
                speak(title)
    else:
        answer = ask_ollama(c)
        print("Jarvis:", answer)
        speak(answer)

if __name__ == "__main__":
    speak("Initializing jarvis...")

    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while True:
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            print("Recognizing...")
            command = recognizer.recognize_google(audio)

            print("You said:", command)
            processCommand(command)

        except sr.UnknownValueError:
            print("I didn't understand. Please speak again.")

        except sr.RequestError as e:
         print("Speech recognition service error:", e)

        except Exception as e:
         print("ERROR TYPE:", type(e).__name__)
         print("ERROR:", repr(e))