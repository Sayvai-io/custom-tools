import pyaudio
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence


def match_target_amplitude(aChunk, target_dBFS):
    """ Normalize given audio chunk """
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)
def record():
    # Constants for audio input
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK_SIZE = 48000

    # Initialize PyAudio
    audio = pyaudio.PyAudio()



    # Open a stream to capture audio from the microphone
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK_SIZE)

    # Create a list to store audio chunks
    audio_chunks = []

    # Recording flag
    recording = False

    # Record audio until interrupted
    try:
        print("Recording... Press Ctrl+C to stop.")
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
                    if len(audio_chunks) > 0:
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
                        for i, chunk in enumerate(chunks):
                            j = j + 1
                            # Print the chunked audio in byte format
                            audio_data_bytes = chunk.raw_data
                            normalized_chunk = match_target_amplitude(audio_data_bytes, -20.0)
                            yield normalized_chunk

                        # Clear the audio chunks list
                        audio_chunks.clear()

                else:
                    # Continue recording audio data
                    audio_chunks.append(data)

            else:
                # Start recording when non-silent audio is detected
                if not is_silence:
                    recording = True
                    audio_chunks.append(data)

    except KeyboardInterrupt:
        print("Recording stopped.")

    finally:
        # Close the audio stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
