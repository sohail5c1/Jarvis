
import speech_recognition as sr
import webbrowser
import pyttsx3  #text to speech
import requests
from openai import OpenAI
#import musicLb
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
#pip install pocketsphinx
import threading
import os


#music links
music = {
    "spring":"https://youtu.be/siCmqvfw_1g?si=6k9vkpPf0pVmTN_Z",
    "mahi":"https://youtu.be/Etkd-07gnxM?si=8x1HCPv98HE2acIK"
}



rec = sr.Recognizer()
engine = pyttsx3.init()  #initializing
newsapi = "{your api}"

def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):
    client = OpenAI(api_keys="{openAi api key}",
    )
    completion = client.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are a virtual assisstant named jarvis skilled in general tasks like like Alexa and google Cloud"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def printCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://twitter.com")
        
        #for music
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link =music[song]
        webbrowser.open(link)

        #for News and api
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")        
    # Check if the request was successful
        if r.status_code == 200:
          data = r.json()
          # Extract and print the headlines
          headlines = data.get('articles', [])
          for article in headlines:
              speak(article.get('title'))
    # for ai
    else:
        output = aiProcess(c)
        speak(output)

def start_drag(event):
    root.x = event.x
    root.y = event.y

def on_drag(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

def setup_window():
    global root, img_tk  # Make root and img_tk global variables
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size and position it at the bottom right corner
    window_size = 120
    root.geometry(f"{window_size}x{window_size}+{screen_width-window_size-10}+{screen_height-window_size-50}")

    # Open the image
    img = Image.open(r"D:\jarviss\label4.webp").convert("RGBA")

    # Create rounded corners
    radius = 20  # adjust the radius as needed
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)

    # # Apply the rounded mask to the image
    img.putalpha(mask)
    rounded_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    rounded_img.paste(img, (0, 0), img)

    img_tk = ImageTk.PhotoImage(rounded_img)

    # Display the image in the label
    panel = tk.Label(root, image=img_tk, bg="white")
    panel.pack(side="bottom", fill="both", expand="yes")

    # Bind dragging functions
    panel.bind("<Button-1>", start_drag)
    panel.bind("<B1-Motion>", on_drag)
              




def voice_rec():
    while True:
        #wake up jarvis
        r = sr.Recognizer()
        #print("recognizing...")

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("listening..")
                audio = r.listen(source) #,timeout=2,phrase_time_limit=2)

            word = r.recognize_google(audio)
            #print(word)
            if (word.lower() == "jarvis"):
                speak("yeah, how can i assist you")
                # Listen for command
                with sr.Microphone() as source:
                    print("jarvis active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    printCommand(command)
                    speak("here we go")


        except Exception as e:
            print("Error: Say again {0}".format(e))



if __name__=="__main__":

    setup_window()
    speak("Initializing jarvis")

    threading.Thread(target=voice_rec, daemon=True).start()
    root.mainloop()
    
