import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import pyjokes
import webbrowser
import wikipedia
import pywhatkit

# Initialize speech recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()
    update_prompt(text)
    print(text)  # Print the spoken text


# Function to update GUI prompt label
def update_prompt(text):
    prompt_text.set(text)

# Function to perform actions based on user input
def perform_action(query):
    if "joke" in query:
        joke = pyjokes.get_joke()
        speak(joke)
        print(joke)

    elif "search" in query:
        query = query.replace("search", "")
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    elif "hello" in query:
        speak("I'm fine, how about you")
        print("I'm fine, how about you")
    elif("play" in query):
       query=query.replace("play","") 
       speak("playing" + query)
       pywhatkit.playonyt(query)

    elif("open aktu" in query):
       speak("opening aktu")
       webbrowser.open("https://aktu.ac.in/")

    elif "wikipedia" in query:
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(result)
    elif "exit" in query:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("Sorry, I didn't understand that.")

# Function to listen to user input
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        status_label.config(text="Listening...", fg="blue")
        root.update()
        audio = recognizer.listen(source)

    try:
        status_label.config(text="Recognizing...", fg="blue")
        root.update()
        query = recognizer.recognize_google(audio, language='en-US')
        user_input_entry.delete(0, tk.END)
        user_input_entry.insert(0, query)
        status_label.config(text="Recognized", fg="green")
        root.update()
        perform_action(query.lower())
    except Exception as e:
        status_label.config(text="Could not understand audio.", fg="red")

# Function to handle button press
def button_pressed():
    query = user_input_entry.get().lower()
    perform_action(query)

# Main GUI setup
root = tk.Tk()
root.title("Virtual Assistant")
root.geometry("600x400")
root.configure(bg='#333333')

prompt_text = tk.StringVar()

frame = tk.Frame(root, bg='#333333')
frame.pack(pady=10, side=tk.BOTTOM, fill=tk.X)

prompt_label = tk.Label(root, textvariable=prompt_text, fg="white", bg='#333333', font=('Arial', 14))
prompt_label.pack()

user_input_entry = tk.Entry(root, width=50, font=('Arial', 14))
user_input_entry.pack(pady=10)

speak_button = tk.Button(frame, text="Speak", command=listen, bg="#4CAF50", fg="white", font=('Arial', 12))
speak_button.pack(side=tk.LEFT, padx=5)

submit_button = tk.Button(frame, text="Submit", command=button_pressed, bg="#008CBA", fg="white", font=('Arial', 12))
submit_button.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 12))
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
