# EchoGate — Sources & References

## Theoretical Foundation

### Stephen Cook — Speech Recognition HOWTO (v2.0, 2002)

**URL:** http://tldp.org/HOWTO/Speech-Recognition-HOWTO/

This foundational document covers:
- ASR (Automatic Speech Recognition) architecture in Linux
- Principles of audio signal digitization
- Hardware considerations for microphone input
- Working with the `/dev/dsp` interface and ALSA

Key quote from the HOWTO:
> Speech recognition is critical for people with repetitive strain injury (RSI), allowing voice to become a full control interface.

This HOWTO is published under the GNU Free Documentation License (GFDL), making it suitable as a reference for open-source projects.

---

## Scientific Justification

### Sarabjeet Singh, Yamini M. — Voice Based Login Authentication For Linux

**Published:** IEEE, 2013  
**URL:** https://ieeexplore.ieee.org/document/...

This paper proves:
- Three-tier authentication is effective for voice-based Linux login
- Random phrase method prevents replay attacks
- Physical presence verification through challenge-response

Key finding: ordinary voice recording can trivially bypass static biometric systems. Dynamic challenge-response with random pass-phrases solves this.

---

## Technical Implementation

### EchoGate Project (2026)

**Repository:** https://github.com/AG064/echogate  
**License:** GPLv3

Documentation on integrating the Vosk lightweight speech recognition engine into LainOS (Arch Linux) through:
- PAM modules (`pam_exec`)
- Python scripts for audio capture
- Vosk for offline speech recognition
- Tkinter for GUI challenge display
- espeak-ng for text-to-speech challenge generation

---

## Technology Choices Explained

### Why Vosk over Whisper?

| Metric | Vosk | Whisper |
|--------|------|---------|
| RAM usage | ~100 MB | Several GB |
| GPU required | No | Yes (CUDA) |
| Offline | Yes | Partial |
| Model size | ~50 MB | ~3 GB |

### Why Python over C++?

- Faster prototyping and iteration
- Easier for students to maintain and modify
- Rich ecosystem for audio processing
- tkinter included with standard Python

### Why GPLv3?

- Guarantees open source (per HOWTO and Linux philosophy)
- Protects against proprietary lock-in
- Requires derivative works to remain open
- Aligned with GNU/Linux ecosystem norms

---

## Audio Parameters Reference

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Channels | 1 (mono) | Sufficient for speech recognition |
| Bit depth | 16-bit | CD quality, low noise floor |
| Sample rate | 16 000 Hz | Optimal for human speech (100 Hz – 8 kHz) |
| Format | WAV / OGG | Lossless / good compression |

Reference: Speech Recognition HOWTO, Section 3 — "How Speech Recognition Works"

---

## Bibliography

1. Cook, S. (2002). *Speech Recognition HOWTO v2.0*. Linux Documentation Project. http://tldp.org/HOWTO/Speech-Recognition-HOWTO/

2. Singh, S., & Yamini, M. (2013). *Voice Based Login Authentication For Linux*. IEEE. https://ieeexplore.ieee.org/document/

3. Alpha掷dex. (2026). *EchoGate Project*. GitHub. https://github.com/AG064/echogate

4. Vosk. (2026). *Offline Speech Recognition*. GitHub. https://github.com/alphacep/vosk-api

5. espeak-ng. (2026). *eSpeak NG Text-to-Speech*. GitHub. https://github.com/espeak-ng/espeak-ng
