# EchoGate

EchoGate is an offline spoken-digit challenge for accessibility experiments. It
recognizes the words spoken, not the identity of the speaker. Any person who can
read or hear the challenge can answer it.

It is not a biometric identity verifier. Keep a normal password or another verified
authentication factor. Do not configure this challenge as a sufficient standalone
PAM login factor. The script's successful exit means only that the challenge matched.

## The "Why"

### Replay Attack Protection

A random challenge changes the words required for each attempt. This does not prove
speaker identity or physical presence and does not prevent synthetic or spliced audio.

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
4. The script reports success only when the spoken digits match the current challenge. This result does not identify the speaker or grant access by itself. A separately verified authentication factor is still required, whether the challenge succeeds or fails.

### OS Integration

`pam_exec` can invoke the script, but its exit status reports only a challenge
match. Do not make this result a sufficient authentication factor or use it to
skip password verification. A failed, unavailable, or successful challenge must
not bypass the separately verified factor required by the login policy.
A complete PAM login flow has not been validated by the focused helper tests.

## Why These Solutions

| Technology | Why this one | Alternative (and why not) |
|---|---|---|
| **Vosk** | ~100MB RAM. Perfect for 4GB systems. | OpenAI Whisper (requires GB of VRAM and CUDA) |
| **Python** | Fast development and easy maintenance for IT students | C++ (harder to maintain and update for custom builds) |
| **GPLv3 / GFDL** | Guarantees open code (per HOWTO principles and Linux philosophy) | Proprietary SDK (vendor lock-in, backdoor risk) |

## Sources

1. **Theoretical foundation:** Stephen Cook, ["Speech Recognition HOWTO" (v2.0, 2002)](http://tldp.org/HOWTO/Speech-Recognition-HOWTO/). Basic guide to ASR (Automatic Speech Recognition) architecture in Linux, audio digitization principles, and hardware.
2. **Historical reference:** Sarabjeet Singh, Yamini M., ["Voice Based Login Authentication For Linux" (IEEE, 2013)](https://ieeexplore.ieee.org/document/...). Retained from the prototype documentation; this placeholder link is unverified and does not establish that EchoGate verifies speaker identity or presence.
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
