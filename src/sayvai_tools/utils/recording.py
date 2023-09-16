import pyaudio
import wave
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Constants for audio input
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 48000

# Initialize PyAudio
audio = pyaudio.PyAudio()


def record():

    def match_target_amplitude(aChunk, target_dBFS):
        """ Normalize given audio chunk """
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)


    # Open a stream to capture audio from the microphone
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,output = False,
                        frames_per_buffer=CHUNK_SIZE)

    # Create a list to store audio chunks
    audio_chunks = []

    # Recording flag
    recording = False

    # Record audio until interrupted
    try:
        j = 0
        while True:
            data = stream.read(CHUNK_SIZE)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Check if audio data is silence
            is_silence = np.max(audio_data) < 100

            if recording:
                if is_silence:
                    # End of an audio chunk
                    recording = False
                    if len(audio_chunks) > 1:
                        # Process the recorded audio chunk
                        song = AudioSegment(
                            data=b"".join(audio_chunks),
                            sample_width=2,
                            frame_rate=RATE,
                            channels=CHANNELS
                        )

                        # Split the chunk on silence
                        chunks = split_on_silence(
                            song,
                            min_silence_len=1000,
                            silence_thresh=-50
                        )
                        silence_chunk = AudioSegment.silent(duration=1000)
                        for i, chunk in enumerate(chunks):
                            j = j + 1
                            # Create a silence chunk that's 0.5 seconds (500 ms) long for padding

                            # Add the padding chunk to the beginning and end of the chunk
                            audio_chunk = silence_chunk + chunk + silence_chunk
                            # Normalize the entire chunk
                            normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
                            # Export the audio chunk with a new bitrate
                            normalized_chunk.export(
                                rf"Recording.mp3",
                                bitrate="192k",
                                format="mp3"
                            )

                        # Clear the audio chunks list
                        audio_chunks.clear()
                        break
                else:
                    # Continue recording audio data
                    audio_chunks.append(data)

            else:
                # Start recording when non-silent audio is detected
                if not is_silence:
                    recording = True
                    audio_chunks.append(data)

        else:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            audio.close(stream=stream)

    except KeyboardInterrupt:
        print("Recording stopped.")