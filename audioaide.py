import pyaudio
import speech_recognition as sr
import whisper

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the OpenAI Whisper engine
# whisper_engine = whisper.Engine()
whisper_model = whisper.load_model("base")

# Start listening to computer audio
with pyaudio.PyAudio() as audio:
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    while True:
        # Get the audio data from the microphone
        data = stream.read(1024)

        # Transcribe the audio data using OpenAI Whisper
        # transcript = whisper_engine.transcribe(data)
        transcript = whisper_model.transcribe(data)

        # Print the transcript to the console
        print(transcript)

        # Check if the user has pressed `q` to quit
        if transcript == "q":
            break

# Close the audio stream
stream.close()