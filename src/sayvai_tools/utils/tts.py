"""TTS file for sayvai_tools."""
from elevenlabs import stream, generate

# elevenlabs.set_api_key("431f452112cab175b80762e50e525c8f")

from elevenlabs import generate, voices
from elevenlabs import save
from elevenlabs.api.voice import Voice
from elevenlabs.simple import VOICES_CACHE, is_voice_id

# from elevenlabs_audio_streaming.constant import VALID_MODELS


class ElevenlabsAudioStreaming:
    
    def __init__(self, api_key) -> None:
        self.api_key =api_key

    @staticmethod
    def check_voice(voice, stability, similarity):
        """
        checks if the voice is available
        Returns: Voice class containing voice_id, name, setting

        """
        if isinstance(voice, str):
            voice_str = voice
        if is_voice_id(voice):
            voice = Voice(voice_id=voice)
        else:
            # Check if voice is in cache
            voice = next((v for v in VOICES_CACHE if v.name == voice_str), None)
            # if the voice not in VOICE_CACHE, call the api to check is voice is available
            if not voice:
                voice = next((v for v in voices() if v.name == voice_str), None) if not voice else voice
        # if voice not found raise ValueError
        if not voice:
            raise ValueError(f"Voice '{voice_str}' not found.")

        voice.settings.stability = stability
        voice.settings.similarity_boost = similarity

    @staticmethod
    def check_model(model):
        """
        checks if the model is available is not
        Returns: value error if model not found

        """

    def audio_streaming(self, text, voice, model, audio_streaming, stability, similarity):
        api_key = self.api_key
        """
        passes the text to elevenlabs api to play the audio

        """
        if not isinstance(audio_streaming, bool):
            raise ValueError(f"Invalid Streaming '{audio_streaming}' value.")

        if not isinstance(text, str):
            raise ValueError("Text input must be a string")

        self.check_voice(voice, stability, similarity)
        self.check_model(model)

        # if Audio streaming is true
        if audio_streaming:
            audio_stream = generate(
                text=text, stream=audio_streaming, voice=voice, model=model, api_key=api_key
            )
            # audio_stream is a generator with byte values that cannot be saved directly using save function
            # so we add all the byte values in generator to a single variable and save the audio
            byte_values = bytearray()
            for byte_chunk in audio_stream:
                byte_values += byte_chunk

            # Convert the accumulated byte values to a bytes object
            final_byte_data = bytes(byte_values)
            return final_byte_data
            # save(final_byte_data, "E:/Text-to-speech/src/audio buffer/audio.wav")
            # play(final_byte_data)

        # if Audio streaming is False
        else:
            audio = generate(
                text=text, voice=voice, model=model, api_key=api_key
            )
            return audio
            # save(audio, "E:/Text-to-speech/src/audio buffer/audio.wav")
            # play(audio)



    @staticmethod
    def avail_voices():
        """
        Returns: returns voice names and corresponding labels

        """
        voice = voices()

        for voice in voice:
            print(voice.name, voice.labels)

