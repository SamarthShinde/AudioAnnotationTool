# converter.py

from pydub import AudioSegment
import os

def convert_to_wav(input_folder, output_folder):
    """
    Converts all audio files in the input_folder to WAV format and saves them in the output_folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_path):
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext != '.wav':
                try:
                    audio = AudioSegment.from_file(input_path)
                    output_file = os.path.join(output_folder, f"{name}.wav")
                    audio.export(output_file, format='wav')
                except Exception as e:
                    print(f"Error converting {filename}: {e}")
            else:
                # Copy WAV files to the output folder
                output_file = os.path.join(output_folder, filename)
                if not os.path.exists(output_file):
                    AudioSegment.from_wav(input_path).export(output_file, format='wav')