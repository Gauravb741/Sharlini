import pyautogui
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import time
import pygetwindow as gw  # Import pygetwindow for window handling
import subprocess  # Import subprocess for opening Chrome profiles

# Initialize the voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Get all available voices
voices = engine.getProperty('voices')
selected_voice = voices[1]  # Change this index to select a different voice
engine.setProperty('voice', selected_voice.id)

# Function to make SHARLINI speak
def speak(text):
    print(f"SHARLINI says: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice commands
def listen(timeout=3, phrase_time_limit=2):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjust very quickly
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("There seems to be an issue with the service.")
            return None

# Function to process commands
def process_command(command):
    global last_song_window  # Variable to store the last window where the song was playing

    if 'open chrome' in command:
        speak("Opening Chrome")
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif 'close chrome' in command:
        speak("Closing Chrome")
        os.system("taskkill /im chrome.exe /f")
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'close youtube' in command:
        close_youtube_tab()
    elif 'play songs' in command:
        speak("Playing the YouTube song playlist.")
        playlist_url = "https://www.youtube.com/watch?v=VYdWSp8pIjg&list=RDVYdWSp8pIjg&start_radio=1&rv=VYdWSp8pIjg"
        webbrowser.open(playlist_url)
        time.sleep(5)
        try:
            last_song_window = next((w for w in gw.getWindowsWithTitle('YouTube') if 'YouTube' in w.title), None)
            if last_song_window:
                last_song_window.activate()
                speak("Now playing the playlist.")
            else:
                speak("Could not locate the YouTube window.")
        except Exception as e:
            speak("Error while activating the YouTube window.")
            print(f"Error: {e}")
    elif 'play current songs' in command:
        if last_song_window:
            try:
                speak("Resuming the song.")
                last_song_window.activate()
                pyautogui.press('space')
            except Exception as e:
                speak("Error while resuming the song.")
                print(f"Error: {e}")
        else:
            speak("No previous song found to play.")
    elif 'stop songs' in command:
        if last_song_window:
            try:
                speak("Stopping the song.")
                last_song_window.activate()
                pyautogui.press('space')  # Simulates pausing the video
                speak("Song stopped.")
            except Exception as e:
                speak("Error while stopping the song.")
                print(f"Error: {e}")
        else:
            speak("No song is currently playing.")
    elif 'sleep' in command:
        speak("Going to sleep mode.")
        return "sleep"
    elif 'fully shutdown' in command:
        speak("Shutting down fully. Goodbye!")
        return "fully shutdown"
    elif 'close current tab' in command:
        close_current_chrome_tab()
    elif 'open personal id' in command:
        open_chrome_profile('Profile 1', 'Personal')
    elif 'open study id' in command:
        open_chrome_profile('Profile 7', 'Study')
    elif 'open college id' in command:
        open_chrome_profile('Profile 3', 'College')
    elif 'my person' in command:
        speak("I love you Aae Baba.")
    elif 'first love' in command:
        speak("RT, I love you three thousand.")
    else:
        speak("I didn't understand the command. Please repeat.")

# Function to open a specific Chrome profile
def open_chrome_profile(profile_dir, profile_name):
    chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Adjust path if needed

    try:
        subprocess.Popen([chrome_path, f"--profile-directory={profile_dir}"])
        speak(f"Opened Chrome with {profile_name} profile.")
    except Exception as e:
        speak(f"Error while opening {profile_name} profile.")
        print(f"Error: {e}")

# Function to close YouTube tab in Chrome
def close_youtube_tab():
    try:
        chrome_windows = gw.getWindowsWithTitle('Chrome')
        for window in chrome_windows:
            if 'YouTube' in window.title:
                window.activate()
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'w')
                speak("Closed the YouTube tab.")
                return
        speak("No YouTube tabs found to close.")
    except Exception as e:
        speak("Error while closing YouTube tab.")
        print(f"Error: {e}")

# Function to close the current Chrome tab
def close_current_chrome_tab():
    try:
        chrome_windows = gw.getWindowsWithTitle('Chrome')
        if not chrome_windows:
            speak("No Chrome windows found.")
            return
        chrome_window = next((w for w in chrome_windows if 'Chrome' in w.title), None)
        if chrome_window:
            chrome_window.activate()
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'w')
            speak("Closed the current Chrome tab.")
        else:
            speak("No visible Chrome window found.")
    except Exception as e:
        speak("Error while closing the current tab.")
        print(f"Error: {e}")

# Main loop for SHARLINI
def main():
    global greeting_done
    if not greeting_done:
        speak("Hello, I am SharLini, your personal assistant. I'm ready for your commands.")
        greeting_done = True

    while True:
        command = listen(timeout=3, phrase_time_limit=2)
        if command:
            result = process_command(command)
            if result == "sleep":
                return "sleep"
            elif result == "fully shutdown":
                return "fully shutdown"

if __name__ == "__main__":
    greeting_done = False
    last_song_window = None
    while True:
        result = main()
        if result == "sleep":
            pass
        elif result == "fully shutdown":
            break
