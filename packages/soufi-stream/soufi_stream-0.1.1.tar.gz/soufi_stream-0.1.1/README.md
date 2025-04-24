# Streamlit Audio Recorder

A customizable audio recorder component for Streamlit applications that automatically segments audio based on silence detection.

## Features

- Real-time audio recording with automatic silence detection
- Configurable silence threshold and timeout
- Returns audio data as base64 encoded string
- Simple and intuitive API

## Installation

```bash
pip install streamlit-audio-recorder
```

## Usage

```python
import streamlit as st
import base64
from streamlit_audio_recorder import audio_recorder

st.title("Audio Recorder Example")

# Basic usage with default parameters
result = audio_recorder()

# Or customized with parameters
result = audio_recorder(
    interval=50,        # hark silence detection interval in ms
    threshold=-60,      # silence threshold in dB
    silenceTimeout=1500 # time of silence before segmenting recording (ms)
)

# Handle the component's return value
if result:
    if result.get('status') == 'stopped':
        audio_data = result.get('audioData')
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            st.audio(audio_bytes, format='audio/webm')
    elif result.get('error'):
        st.error(f"Error: {result.get('error')}")
```

## Configuration Parameters

- `interval` (int): Time in milliseconds between checks for silence (default: 50)
- `threshold` (int): Volume threshold in dB to detect silence (default: -60)
- `play` (bool): Whether to play back the audio during recording (default: False)
- `silenceTimeout` (int): Time in milliseconds of silence before stopping a segment (default: 1500)

## License

MIT