# EchoGate

**Echogate** is your entry point into the wired. Voice-based challenge-response authentication using your voice. Works fully offline.

## The "Why"

### Replay Attack Protection

As documented by Sarabjeet Singh & Yamini M. in their [IEEE paper (2013)](https://ieeexplore.ieee.org/document/...), ordinary voice recording can easily bypass biometric systems. Using a **Random Pass-phrase** guarantees the physical presence of the user at login time.

### Inclusivity

As Stephen Cook notes in his [Speech Recognition HOWTO (2002)](http://tldp.org/HOWTO/Speech-Recognition-HOWTO/), ASR is critical for people with disabilities (RSI, dystrophy), turning voice into a full control tool.

### Privacy

Unlike modern cloud solutions, EchoGate works **completely offline** — no voice samples are ever sent to external servers.

## Technical Details

### Audio Parameters

Following the HOWTO recommendations:
- Mono signal, 16-bit depth, 16kHz sample rate
- Optimal for human speech (100Hz–8kHz range)

### Algorithm: Challenge-Response

1. System generates 3 random numbers
2. Python script speaks them aloud (via `espeak-ng`) and displays GUI (Tkinter)
3. Vosk engine recognizes the user's response in real time
4. `pam_exec` integration — if voice matches the challenge, access is granted. If not, silently falls back to standard password input

### OS Integration

Execution via `pam_exec`. Login flow is transparent to the user — works alongside standard Linux authentication.

## Why These Solutions

| Technology | Why this one | Alternative (and why not) |
|---|---|---|
| **Vosk** | ~100MB RAM. Perfect for 4GB systems. | OpenAI Whisper (requires GB of VRAM and CUDA) |
| **Python** | Fast development and easy maintenance for IT students | C++ (harder to maintain and update for custom builds) |
| **GPLv3 / GFDL** | Guarantees open code (per HOWTO principles and Linux philosophy) | Proprietary SDK (vendor lock-in, backdoor risk) |

## Sources

1. **Theoretical foundation:** Stephen Cook, ["Speech Recognition HOWTO" (v2.0, 2002)](http://tldp.org/HOWTO/Speech-Recognition-HOWTO/). Basic guide to ASR (Automatic Speech Recognition) architecture in Linux, audio digitization principles, and hardware.
2. **Scientific justification:** Sarabjeet Singh, Yamini M., ["Voice Based Login Authentication For Linux" (IEEE, 2013)](https://ieeexplore.ieee.org/document/...). Paper proving the effectiveness of three-tier authentication and random phrase method for Replay attack protection.
3. **Technical implementation:** EchoGate Project (2026). Documentation on integrating the lightweight Vosk engine into LainOS (Arch Linux) via PAM modules and Python.

## Project Structure

```
echogate/
├── README.md          # This file
├── SOURCES.md         # Detailed references and bibliography
├── LICENSE            # GPLv3
├── echogate.py        # Main authentication script
├── PKGBUILD           # Arch Linux package build
```

## Dependencies

- `vosk` — offline speech recognition
- `espeak-ng` — text-to-speech for challenge generation
- `python-pam` or `pam_exec` — Linux PAM integration
- Tkinter (included with Python)

## License

GPLv3
