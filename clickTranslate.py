import time
import pyperclip
from langdetect import detect
from googletrans import Translator
from pynput import mouse, keyboard

click_count = 0
last_click_time = 0
text = ""

key = keyboard.Controller()     # key variable for Keyboard Detection module
translator = Translator()       # translator varable for Translator module
listener = None                 # Global variable for the mouse listener

# Detect the language to use as source for translator
def detector(content):
    language = detect(content)
    return language

# Translating mechanism
def langTranslate(content):
    lang = detector(content)
    translation = translator.translate(text, src=lang, dest='en')
    pyperclip.copy(translation.text)
    # Copy the returning translated text to clipboard

# Autocopy after Triple Click
def simulate_copy():
    time.sleep(0.5)
    with key.pressed(keyboard.Key.ctrl):
        key.press('c')
        key.release('c')
    time.sleep(0.2)

# Triple Click Counter, Copy Selection, Paste to Variable, Translator Mechanism + Clipboard Paste
def on_click(x, y, button, pressed):
    global click_count, last_click_time, text
    if pressed:
        current_time = time.perf_counter()
        if current_time - last_click_time < 0.5:
            click_count += 1
            if click_count == 3:
                simulate_copy()
                try:
                    text = pyperclip.paste()
                    langTranslate(text)
                except Exception as e:
                    print(f"Error copying to clipboard: {e}")
        else:
            click_count = 1
        last_click_time = current_time

# Termination with Esc
def on_key_press(key):
    global listener
    if key == keyboard.Key.esc:
        print("Esc key pressed. Stopping...")
        if listener:
            listener.stop()

# Set up the keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_key_press)
keyboard_listener.start()

# Set up the mouse listener
listener = mouse.Listener(on_click=on_click)
listener.start()

# Block until the listener is stopped
listener.join()
