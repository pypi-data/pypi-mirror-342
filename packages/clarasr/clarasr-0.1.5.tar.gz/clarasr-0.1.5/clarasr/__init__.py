"""
ClaraSR - A Python package for speech recognition and command processing.

This package provides a simple interface for continuous speech recognition with wake word detection.
"""

from .main import (
    config,
    startup,
    get,
    get_clean,
    exit,
    AudioSegment,
    detect_silence,
    contains_wake_word,
    find_wake_word_position,
    extract_command
)

__version__ = "0.1.0"
__author__ = "Kiko"

__all__ = [
    'config',
    'startup',
    'get',
    'get_clean',
    'exit',
    'AudioSegment',
    'detect_silence',
    'contains_wake_word',
    'find_wake_word_position',
    'extract_command'
] 