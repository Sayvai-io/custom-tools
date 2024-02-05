# import io

# import numpy as np
# # import pyaudio
# # from pydub import AudioSegment
# # from pydub.silence import split_on_silence

# # Constants for TTS input
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK_SIZE = 16000

# # Initialize PyAudio
# audio = pyaudio.PyAudio()


# def record():
#     def match_target_amplitude(aChunk, target_dBFS):
#         """Normalize given TTS chunk"""
#         change_in_dBFS = target_dBFS - aChunk.dBFS
#         return aChunk.apply_gain(change_in_dBFS)

#     # Open a stream to capture TTS from the microphone
#     stream = audio.open(
#         format=FORMAT,
#         channels=CHANNELS,
#         rate=RATE,
#         input=True,
#         output=False,
#         frames_per_buffer=CHUNK_SIZE,
#     )

#     # Create a list to store TTS chunks
#     audio_chunks = []

#     # Recording flag
#     recording = False

#     # Record TTS until interrupted
#     try:
#         j = 0
#         while True:
#             data = stream.read(CHUNK_SIZE)
#             audio_data = np.frombuffer(data, dtype=np.int16)

#             # Check if TTS data is silence
#             is_silence = np.max(audio_data) < 350
#             # print(np.max(audio_data))

#             if recording:
#                 if is_silence:
#                     # End of an TTS chunk
#                     recording = False
#                     if len(audio_chunks) > 0:
#                         # Process the recorded TTS chunk
#                         song = AudioSegment(
#                             data=b"".join(audio_chunks),
#                             sample_width=2,
#                             frame_rate=RATE,
#                             channels=CHANNELS,
#                         )

#                         # Split the chunk on silence
#                         chunks = split_on_silence(
#                             song, min_silence_len=1500, silence_thresh=-35
#                         )
#                         silence_chunk = AudioSegment.silent(duration=500)
#                         combined_chunks = AudioSegment.empty()
#                         for i in chunks:
#                             combined_chunks += i

#                         # Create a silence chunk that's 0.5 seconds (500 ms) long for padding
#                         audio_chunk = silence_chunk + combined_chunks + silence_chunk
#                         # Normalize the entire chunk
#                         normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

#                         # Export the TTS chunk with a new bitrate
#                         mp3_buffer = io.BytesIO()
#                         normalized_chunk.export(
#                             mp3_buffer, format="mp3", bitrate="192k"
#                         )

#                         mp3_bytes = mp3_buffer.getvalue()
#                         mp3_buffer.close()
#                         return mp3_bytes

#                         # Clear the TTS chunks list
#                         audio_chunks.clear()

#                         break
#                 else:
#                     # Continue recording TTS data
#                     audio_chunks.append(data)

#             else:
#                 # Start recording when non-silent TTS is detected
#                 if not is_silence:
#                     recording = True
#                     audio_chunks.append(data)

#         else:
#             stream.stop_stream()
#             stream.close()
#             audio.terminate()
#             audio.close(stream=stream)

#     except KeyboardInterrupt:
#         print("Recording stopped.")


class Recording:
    raise "NotImplementedError"
