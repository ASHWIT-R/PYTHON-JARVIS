
import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import os
import re
import ast
import operator
from datetime import datetime


# ==================================================
# VOICE ENGINE
# ==================================================

engine = pyttsx3.init()

# Voice settings
engine.setProperty("rate", 170)
engine.setProperty("volume", 200.0)


def speak(message):
    """Make Jarvis speak and also show the message on screen."""
    print("JARVIS:", message)

    engine.say(message)
    engine.runAndWait()


# ==================================================
# LISTEN TO USER
# ==================================================

def listen():
    """Listen to the user's voice and convert it into text."""

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")

        # Adjust microphone according to background noise
        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            command = recognizer.recognize_google(audio)

            print("YOU:", command)

            return command.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""

        except sr.RequestError:
            speak("The speech recognition service is not available.")
            return ""


# ==================================================
# WINDOWS APPLICATIONS
# ==================================================

apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
}


def open_app(command):
    """Check whether the user wants to open a Windows application."""

    for app_name, app_path in apps.items():

        if app_name in command:

            speak(f"Opening {app_name}")

            try:
                subprocess.Popen(app_path)

            except Exception:
                speak(f"Sorry, I couldn't open {app_name}")

            return True

    return False


# ==================================================
# WEBSITES
# ==================================================

websites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
}


def open_website(command):
    """Open a website when the user asks for it."""

    for website_name, website_url in websites.items():

        if website_name in command:

            speak(f"Opening {website_name}")

            webbrowser.open(website_url)

            return True

    return False

    
# ==================================================
# WINDOWS FOLDERS
# ==================================================

folders = {
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "desktop": os.path.expanduser("~/Desktop"),
    "pictures": os.path.expanduser("~/Pictures"),
    "music": os.path.expanduser("~/Music"),
    "videos": os.path.expanduser("~/Videos"),
}


def open_folder(command):
    """Open a Windows folder."""

    for folder_name, folder_path in folders.items():

        if folder_name in command:

            speak(f"Opening {folder_name}")

            try:
                os.startfile(folder_path)

            except Exception:
                speak(f"Sorry, I couldn't open {folder_name}")

            return True

    return False


# ==================================================
# SAFE CALCULATOR
# ==================================================

# Allowed mathematical operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}


def calculate_node(node):
    """Calculate a mathematical expression safely."""

    # Numbers
    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError

    # Addition, subtraction, multiplication, etc.
    if isinstance(node, ast.BinOp):

        left = calculate_node(node.left)
        right = calculate_node(node.right)

        operation = operators.get(type(node.op))

        if operation is None:
            raise ValueError

        return operation(left, right)

    # Positive and negative numbers
    if isinstance(node, ast.UnaryOp):

        value = calculate_node(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

    raise ValueError


def calculate_expression(expression):
    """Turn a mathematical expression into an answer."""

    try:
        tree = ast.parse(expression, mode="eval")

        return calculate_node(tree.body)

    except Exception:
        return None


def do_calculation(command):
    """Understand a voice calculation and calculate the answer."""

    expression = command

    # Remove unnecessary words
    words_to_remove = [
        "calculate",
        "what is",
        "what's",
        "please"
    ]

    for word in words_to_remove:
        expression = expression.replace(word, "")

    # Convert spoken math into mathematical symbols
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("multiply by", "*")
    expression = expression.replace("times", "*")

    expression = expression.replace("divided by", "/")
    expression = expression.replace("divide by", "/")

    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")

    expression = expression.replace("mod", "%")
    expression = expression.replace("power", "**")

    # Remove anything that is not needed for calculation
    expression = re.sub(
        r"[^0-9+\-*/%.() ]",
        "",
        expression
    )

    expression = expression.strip()

    if not expression:
        speak("I couldn't find a calculation.")
        return

    result = calculate_expression(expression)

    if result is None:
        speak("Sorry, I couldn't calculate that.")

    else:
        speak(f"The answer is {result}")


# ==================================================
# GOOGLE SEARCH
# ==================================================

def search_google(command):
    """Search Google using the user's voice command."""

    search_text = command.replace(
        "search",
        "",
        1
    ).strip()

    if not search_text:
        speak("What would you like me to search for?")
        return

    speak(f"Searching Google for {search_text}")

    search_url = (
        "https://www.google.com/search?q="
        + search_text.replace(" ", "+")
    )

    webbrowser.open(search_url)


# ==================================================
# TIME
# ==================================================

def tell_time():
    """Tell the current time."""

    current_time = datetime.now().strftime("%I:%M %p")

    speak(f"The time is {current_time}")


# ==================================================
# MAIN JARVIS PROGRAM
# ==================================================

def jarvis():

    speak("Hello Captain. I am Jarvis. How can I help you?")

    while True:

        command = listen()

        # If nothing was heard, listen again
        if command == "":
            continue

        # ------------------------------------------------
        # GREETING
        # ------------------------------------------------

        if "hello" in command or "hi jarvis" in command:

            speak("Hello Captain. How can I help you?")

        # ------------------------------------------------
        # CALCULATOR
        # ------------------------------------------------

        elif (
            "calculate" in command
            or "what is" in command
            or "what's" in command
        ):

            do_calculation(command)

        # ------------------------------------------------
        # TIME
        # ------------------------------------------------

        elif "time" in command:

            tell_time()

        # ------------------------------------------------
        # OPEN SOMETHING
        # ------------------------------------------------

        elif "open" in command:

            # Try opening a Windows application
            if open_app(command):
                continue

            # Try opening a website
            if open_website(command):
                continue

            # Try opening a folder
            if open_folder(command):
                continue

            speak("Sorry, I couldn't find what you asked me to open.")

        # ------------------------------------------------
        # GOOGLE SEARCH
        # ------------------------------------------------

        elif "search" in command:

            search_google(command)

        # ------------------------------------------------
        # EXIT JARVIS
        # ------------------------------------------------

        elif (
            "stop" in command
            or "exit" in command
            or "quit" in command
            or "goodbye" in command
        ):

            speak("Goodbye Captain. Have a great day!")

            break

        # ------------------------------------------------
        # UNKNOWN COMMAND
        # ------------------------------------------------

        else:

            speak("I don't know that command yet.")


# ==================================================
# END OF PROGRAM
# ==================================================
