# ClaraSR

A Python package for speech recognition and command processing with wake word detection.

## Features

- Continuous speech recognition
- Configurable wake word detection
- Real-time audio processing
- Command extraction and processing
- Simple and intuitive API

## Installation

```bash
pip install clarasr
```

## Requirements

- Python 3.6 or higher
- PyAudio
- SpeechRecognition
- NumPy
- PyTorch
- Requests

## Quick Start

```python
from clarasr import config, startup, get, exit

# Configure the system (optional)
config(wake_word="clara", energy_threshold=1000)

# Start the speech recognition system
startup()

try:
    while True:
        # Get the latest recognized text
        text = get()
        if text:
            print(f"Recognized: {text}")
        time.sleep(0.1)
except KeyboardInterrupt:
    # Clean up and exit
    exit()
```

## API Reference

### Configuration

```python
config(
    wake_word="clara",           # The word to trigger command processing
    energy_threshold=1000,       # Audio energy threshold for silence detection
    processing_delay=1.5,        # Delay between wake word detections (seconds)
    min_command_length=3         # Minimum words for a valid command
)
```

### Core Functions

- `startup()`: Start the speech recognition system
- `get()`: Get the latest recognized text
- `exit()`: Stop the speech recognition system

### Advanced Usage

```python
from clarasr import (
    AudioSegment,
    detect_silence,
    contains_wake_word,
    find_wake_word_position,
    extract_command,
    process_command
)

# Example of custom command processing
def custom_process_command(command):
    if command:
        print(f"Processing custom command: {command}")
        return True
    return False

# Configure and start the system
config(wake_word="assistant")
startup()

try:
    while True:
        text = get()
        if text:
            # Custom command processing
            if contains_wake_word(text, "assistant"):
                command = extract_command([AudioSegment(text, datetime.now(), b"")], "assistant")
                if command:
                    custom_process_command(command)
        time.sleep(0.1)
except KeyboardInterrupt:
    exit()
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.