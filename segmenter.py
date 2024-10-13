# segmenter.py

from pydub import AudioSegment
import math

def segment_audio(file_path, segment_length=5000):
    """
    Splits an audio file into segments of specified length (in milliseconds).
    Returns a list of (start_time, end_time) tuples.
    """
    audio = AudioSegment.from_wav(file_path)
    duration_ms = len(audio)
    segments = []
    for i in range(0, duration_ms, segment_length):
        start = i
        end = min(i + segment_length, duration_ms)
        segments.append((start, end))
    return segments