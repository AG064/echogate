#!/usr/bin/env python3
"""
EchoGate - Voice-based authentication for Arch Linux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import os

# Add custom library path for vosk installed via pip
sys.path.append("/opt/echogate/libs")
MODEL_PATH = "/opt/echogate/model"

import random
import subprocess
import json

import sounddevice as sd
from vosk import Model, KaldiRecognizer

SAMPLE_RATE = 16000
LISTEN_DURATION = 5  # seconds

# GUI globals
gui_root = None
gui_label = None
gui_running = False


def is_tty_session():
    """Check if running in a TTY/Terminal session."""
    try:
        return os.isatty(sys.stdin.fileno())
    except (OSError, ValueError):
        return False


def is_sudo_session():
    """Check if running via sudo."""
    # Check if SUDO_USER environment variable is set
    return os.environ.get("SUDO_USER") is not None


def should_use_gui():
    """Determine if GUI should be used based on session type."""
    # If running in TTY or via sudo, don't use GUI
    if is_tty_session() or is_sudo_session():
        return False
    # Use GUI when running from Display Manager (no TTY present)
    return True


def create_gui():
    """Create the GUI window in a separate thread."""
    global gui_root, gui_label, gui_running
    
    try:
        import tkinter as tk
    except ImportError:
        return False
    
    gui_running = True
    
    gui_root = tk.Tk()
    gui_root.title("EchoGate")
    
    # Remove window decorations for overlay effect
    gui_root.overrideredirect(True)
    
    # Set window size and center on screen
    window_width = 400
    window_height = 150
    screen_width = gui_root.winfo_screenwidth()
    screen_height = gui_root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    gui_root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Cyberpunk/Lain style: black background, green text
    gui_root.configure(bg="black")
    
    # Create main label
    gui_label = tk.Label(
        gui_root,
        text="System Check...",
        font=("Courier", 18, "bold"),
        fg="#00ff00",  # Bright green
        bg="black"
    )
    gui_label.pack(expand=True, fill="both")
    
    # Keep window on top
    gui_root.attributes("-topmost", True)
    
    return True


def update_gui(message):
    """Update the GUI label with a new message."""
    global gui_root, gui_label
    if gui_root and gui_label:
        try:
            gui_label.config(text=message)
            gui_root.update()
        except Exception:
            pass


def close_gui():
    """Close the GUI window."""
    global gui_root, gui_running
    if gui_root:
        try:
            gui_root.destroy()
        except Exception:
            pass
    gui_running = False


def generate_digits(count=3):
    """Generate a string of random digits."""
    return "".join(str(random.randint(0, 9)) for _ in range(count))


def speak_digits(digits, use_gui=False):
    """Speak the given digits using espeak-ng."""
    # Speak each digit separately for clarity
    text = " ".join(digits)
    
    if use_gui:
        update_gui(f"SAY: {text}")
    
    try:
        subprocess.run(["espeak-ng", text], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to run espeak-ng: {e}", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)
    except FileNotFoundError:
        print("Error: espeak-ng not found. Please install espeak-ng.", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)


def listen_for_speech(duration=LISTEN_DURATION, use_gui=False):
    """Listen for speech and return recognized text."""
    if use_gui:
        update_gui("Listening...")
    
    # Load the speech recognition model
    if not os.path.isdir(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)

    try:
        model = Model(MODEL_PATH)
    except Exception as e:
        print(f"Error: Failed to load speech model: {e}", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)

    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    # Calculate the number of samples to record
    num_samples = int(duration * SAMPLE_RATE)

    # Record audio
    try:
        audio = sd.rec(num_samples, samplerate=SAMPLE_RATE, channels=1, dtype="int16")
        sd.wait()
    except sd.PortAudioError as e:
        print(f"Error: Audio device error: {e}", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to record audio: {e}", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)

    # Process the recorded audio
    recognizer.AcceptWaveform(audio.tobytes())
    result = json.loads(recognizer.FinalResult())

    return result.get("text", "")


def extract_digits(text):
    """Extract digits from recognized text (handles both numeric and word forms)."""
    word_to_digit = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
        "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
    }

    digits = []
    for word in text.lower().split():
        if word in word_to_digit:
            digits.append(word_to_digit[word])

    return "".join(digits)


def run_auth(use_gui=False):
    """Run the authentication process."""
    # Generate random digits
    expected_digits = generate_digits(3)

    # Speak the digits
    speak_digits(expected_digits, use_gui)

    # Listen for user response
    recognized_text = listen_for_speech(LISTEN_DURATION, use_gui)

    # Extract digits from recognized speech
    recognized_digits = extract_digits(recognized_text)

    # Compare and return result
    return recognized_digits == expected_digits


def main():
    """Main entry point."""
    use_gui = should_use_gui()
    
    # If running in TTY/sudo session, exit immediately to fall back to password
    if not use_gui:
        sys.exit(1)
    
    # Create and show GUI
    if use_gui:
        if not create_gui():
            # If GUI creation fails, exit to fall back to password
            sys.exit(1)
    
    try:
        # Run authentication
        success = run_auth(use_gui)
        
        if use_gui:
            if success:
                update_gui("ACCESS GRANTED")
            else:
                update_gui("ACCESS DENIED")
            # Brief pause to show result
            import time
            time.sleep(1)
            close_gui()
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if use_gui:
            close_gui()
        sys.exit(1)


if __name__ == "__main__":
    main()
