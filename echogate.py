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
LIBS_PATH = "/opt/echogate/libs"
if os.path.isdir(LIBS_PATH):
    sys.path.insert(0, LIBS_PATH)

import random
import subprocess
import json

import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = "/opt/echogate/model"
SAMPLE_RATE = 16000
LISTEN_DURATION = 5  # seconds


def generate_digits(count=3):
    """Generate a string of random digits."""
    return "".join(str(random.randint(0, 9)) for _ in range(count))


def speak_digits(digits):
    """Speak the given digits using espeak-ng."""
    # Speak each digit separately for clarity
    text = " ".join(digits)
    subprocess.run(["espeak-ng", text], check=True)


def listen_for_speech(duration=LISTEN_DURATION):
    """Listen for speech and return recognized text."""
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    # Calculate the number of samples to record
    num_samples = int(duration * SAMPLE_RATE)

    # Record audio
    audio = sd.rec(num_samples, samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()

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


def main():
    """Main entry point."""
    # Generate random digits
    expected_digits = generate_digits(3)

    # Speak the digits
    speak_digits(expected_digits)

    # Listen for user response
    recognized_text = listen_for_speech(LISTEN_DURATION)

    # Extract digits from recognized speech
    recognized_digits = extract_digits(recognized_text)

    # Compare and exit with appropriate code
    if recognized_digits == expected_digits:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
