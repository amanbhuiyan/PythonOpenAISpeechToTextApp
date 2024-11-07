'''

import sounddevice as sd
import numpy as np
import os
import keyboard  # To detect shortcut key press
from pydub import AudioSegment
from openai import OpenAI
import os
from dotenv import load_dotenv

from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)


import sounddevice as sd

def record_audio(duration=10, sample_rate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    return recording



from pydub import AudioSegment
import numpy as np
import os

def save_as_mp3(audio_data, sample_rate=44100, file_name='output.mp3', folder='audio'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    full_path = os.path.join(folder, file_name)
    audio_segment = AudioSegment(
        data=np.array(audio_data).tobytes(),
        sample_width=2,
        frame_rate=sample_rate,
        channels=2
    )
    audio_segment.export(full_path, format='mp3')
    return full_path



from openai import OpenAI

def transcribe_audio(file_path):
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='en'
        )
    print(f'Transcription: {transcription.text}')








load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def record_audio(duration=5, sample_rate=44100):
    """Record audio from the microphone."""
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished")
    return recording

def save_as_mp3(audio_data, sample_rate=44100, file_name='output.mp3', folder='audio'):

    print("""Save recorded audio as MP3 in a specified folder.""")
    if not os.path.exists(folder):
        os.makedirs(folder)
    full_path = os.path.join(folder, file_name)
    print(full_path)
    audio_segment = AudioSegment(
        data=np.array(audio_data).tobytes(),
        sample_width=2,  # 2 bytes (16 bits) per sample
        frame_rate=sample_rate,
        channels=2
    )
    

    print("Her is the full path")
    print(full_path)
    audio_segment.export(full_path, format='mp3')
    return full_path

def transcribe_audio(file_path):
    """Transcribe the audio file using OpenAI's API."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='en'
        )
    print(f'Transcription :{transcription.text}')

if __name__ == "__main__":
    sample_rate = 44100  # Sample rate in Hz
    duration = 5  # Duration of recording in seconds
    try:
        while True:
            if keyboard.is_pressed('esc'):  # Check if ESC key is pressed to exit
                print("Exiting...")
                break
            audio_data = record_audio(duration, sample_rate)
            file_path = save_as_mp3(audio_data, sample_rate)
            print("File path ---------------------")
            print(file_path)
            transcribe_audio(file_path)
    except KeyboardInterrupt:
        print("Program terminated.")




        
'''

import os
import numpy as np
import sounddevice as sd
from flask import Flask, render_template, jsonify, request
from pydub import AudioSegment
import openai
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')

#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Path to save audio recordings
AUDIO_DIR = 'audio'
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

sample_rate = 44100  # Sample rate in Hz
duration = 5  # Duration of recording in seconds

def record_audio():
    """Record audio from the microphone."""
    print("Recording...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished")
    return recording

def save_as_mp3(audio_data, sample_rate=44100):
    """Save recorded audio as MP3."""
    file_name = 'output.mp3'
    full_path = os.path.join(AUDIO_DIR, file_name)
    audio_segment = AudioSegment(
        data=np.array(audio_data).tobytes(),
        sample_width=2,
        frame_rate=sample_rate,
        channels=2
    )
    audio_segment.export(full_path, format='mp3')
    return full_path

def transcribe_audio(file_path):
    """Transcribe the audio file using OpenAI's Whisper API."""
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
    return response['text']


def transcribe_audio(file_path):
    """Transcribe the audio file using OpenAI's API."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language='en'
        )

        print(f'Transcription :{transcription.text}')

        return transcription.text
    




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    audio_data = record_audio()
    file_path = save_as_mp3(audio_data, sample_rate)
    transcription_text = transcribe_audio(file_path)
    print("+++++++++++++++++++++++")
    print(transcription_text)
    return jsonify({'transcription': transcription_text})


if __name__ == '__main__':
    app.run(debug=True)
