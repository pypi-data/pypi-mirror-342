import queue
import threading
import sys
import time
import torch
import numpy as np
import speech_recognition as sr
import logging
from datetime import datetime
from collections import deque
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables
recognized_text = ""
is_running = False
transcribe_thread = None
segments = deque(maxlen=15)  # Store last 15 seconds of speech
wake_word = "clara"
energy_threshold = 1000
processing_delay = 1.5
min_command_length = 3
last_text = ""  # Track the last text that was returned

class AudioSegment:
    def __init__(self, text, timestamp, audio_data):
        self.text = text
        self.timestamp = timestamp
        self.audio_data = audio_data

def config(new_wake_word="clara", new_energy_threshold=1000, new_processing_delay=1.5, new_min_command_length=3):
    """Configure the speech recognition system parameters."""
    global wake_word, energy_threshold, processing_delay, min_command_length
    wake_word = new_wake_word
    energy_threshold = new_energy_threshold
    processing_delay = new_processing_delay
    min_command_length = new_min_command_length
    logging.info(f"Configuration updated: wake_word={wake_word}, energy_threshold={energy_threshold}")

def detect_silence(audio_data):
    """Detects silence based on audio energy."""
    try:
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        energy = np.abs(audio_np).mean()
        return energy < energy_threshold
    except Exception as e:
        logging.error(f"Error in silence detection: {e}")
        return False

def contains_wake_word(text, wake_word):
    """Check if the text contains the wake word, handling potential variations."""
    try:
        words = text.lower().split()
        return any(wake_word in word for word in words)
    except Exception as e:
        logging.error(f"Error in wake word detection: {e}")
        return False

def find_wake_word_position(text, wake_word):
    """Find the position of the wake word in the text."""
    try:
        text = text.lower()
        wake_word = wake_word.lower()
        
        pos = text.find(wake_word)
        if pos != -1:
            return pos
        
        for i in range(len(text) - len(wake_word) + 1):
            if text[i:i+len(wake_word)] == wake_word:
                return i
        
        return -1
    except Exception as e:
        logging.error(f"Error finding wake word position: {e}")
        return -1

def extract_command(segments, wake_word):
    """Extract the command from segments between wake word and silence."""
    try:
        if not segments:
            return ""
        
        segments_list = list(segments)
        wake_segment = None
        wake_pos = -1
        
        for i, segment in enumerate(segments_list):
            pos = find_wake_word_position(segment.text, wake_word)
            if pos != -1:
                wake_segment = segment
                wake_pos = pos
                break
        
        if wake_segment is None:
            return ""
        
        command_parts = [wake_segment.text[wake_pos + len(wake_word):].strip()]
        
        for segment in segments_list[i+1:]:
            command_parts.append(segment.text)
        
        full_command = " ".join(command_parts).strip()
        
        if len(full_command.split()) < min_command_length:
            return ""
        
        return full_command
    except Exception as e:
        logging.error(f"Error extracting command: {e}")
        return ""

def transcribe_audio():
    """Main transcription loop."""
    global recognized_text, is_running, segments, last_text
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    last_wake_detection = 0
    
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            logging.info("Listening continuously...")
            
            while is_running:
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    timestamp = datetime.now()
                    
                    try:
                        text = recognizer.recognize_google(audio).strip()
                    except sr.UnknownValueError:
                        text = ""
                    except sr.RequestError as e:
                        logging.error(f"Error with Google Speech Recognition: {e}")
                        text = ""
                    
                    if text and text != last_text:
                        last_text = text
                        segments.append(AudioSegment(text, timestamp, audio.get_raw_data()))
                        recent_text = " ".join(seg.text for seg in segments).lower()
                        
                        if contains_wake_word(recent_text, wake_word):
                            current_time = time.time()
                            if current_time - last_wake_detection >= processing_delay:
                                last_wake_detection = current_time
                                command = extract_command(segments, wake_word)
                                if command:
                                    logging.info(f"Command detected: {command}")
                                    segments.clear()
                                    time.sleep(2)  # Prevent immediate re-processing
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    logging.error(f"Error processing audio: {e}")
                    continue
                    
    except Exception as e:
        logging.error(f"Fatal error in audio processing: {e}")
        is_running = False

def startup():
    """Start the speech recognition system."""
    global is_running, transcribe_thread
    if not is_running:
        is_running = True
        transcribe_thread = threading.Thread(target=transcribe_audio, daemon=True)
        transcribe_thread.start()
        logging.info("Speech recognition system started")
        return True
    return False

def get():
    """Get the latest recognized text."""
    global segments
    if segments:
        return segments[-1].text
    return ""

def get_clean():
    """Get the latest recognized text without the wake word."""
    global segments, wake_word
    if segments:
        text = segments[-1].text
        # Remove the wake word from the text
        text = text.lower().replace(wake_word.lower(), "", 1).strip()
        return text
    return ""

def exit():
    """Stop the speech recognition system."""
    global is_running, transcribe_thread
    if is_running:
        is_running = False
        if transcribe_thread:
            transcribe_thread.join(timeout=1.0)
        logging.info("Speech recognition system stopped")
        return True
    return False

if __name__ == "__main__":
    startup()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
