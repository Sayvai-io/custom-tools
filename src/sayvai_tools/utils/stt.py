import yaml
import os
from google.cloud import speech_v1p1beta1 as speech
from sayvai_tools.utils.recording import record


# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "G_Cloud_API_key.json"


class STT:
    def __init__(self, model: str = "default", sample_rate: int = 44100, lang_code: str = "en-IN",
                 automatic_punctuation: bool = True,
                 enhanced: bool = True,
                 second_lang_codes: list[str] = ["en-US"], no_of_audio_channels: int = 2,
                 sep_rec_per_channel: bool = True, spoken_punctuation: bool = True,
                 word_confidence: bool = True, spoken_emoji: bool = True,
                 max_alt: int = 0, audio_format: str = "default", interact_type: str = "default",
                 naics_code: int | None = None, mic_distance: str = "default", media_type: str = "default",
                 record_device_type: str = "default", record_device_name: str | None = None,
                 audio_topic: str = "general", speech_context_path: str | None = None):
        self.model = model
        self.sample_rate_hertz = sample_rate
        self.language_code = lang_code
        self.enable_automatic_punctuation = automatic_punctuation
        self.use_enhanced = enhanced
        self.alternate_language_codes = second_lang_codes
        self.audio_channel_count = no_of_audio_channels
        self.enable_separate_recognition_per_channel = sep_rec_per_channel
        self.enable_spoken_punctuation = spoken_punctuation
        self.enable_spoken_emojis = spoken_emoji
        self.max_alternatives = max_alt
        self.audio_format = audio_format
        self.enable_word_confidence = word_confidence
        self.interaction_type = interact_type
        self.naics_code = naics_code
        self.microphone_distance = mic_distance
        self.original_media_type = media_type
        self.recording_device_type = record_device_type
        self.recording_device_name = record_device_name
        self.audio_topic = audio_topic
        self.speech_context_path = speech_context_path
        self.state = True

    def audio_encoding(self):
        if self.audio_format == "mp3":
            return speech.RecognitionConfig.AudioEncoding.MP3
        elif self.audio_format == "flac":
            return speech.RecognitionConfig.AudioEncoding.FLAC
        elif self.audio_format == "l16":
            return speech.RecognitionConfig.AudioEncoding.LINEAR16
        elif self.audio_format == "mulaw":
            return speech.RecognitionConfig.AudioEncoding.MULAW
        elif self.audio_format == "amr":
            return speech.RecognitionConfig.AudioEncoding.AMR
        elif self.audio_format == "amr-wb":
            return speech.RecognitionConfig.AudioEncoding.AMR_WB
        elif self.audio_format == "ogg-opus":
            return speech.RecognitionConfig.AudioEncoding.OGG_OPUS
        elif self.audio_format == "speex":
            return speech.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE
        elif self.audio_format == "webm-opus":
            return speech.RecognitionConfig.AudioEncoding.WEBM_OPUS
        else:
            return speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED

    def create_reg_config(self):

        config_mp3 = speech.RecognitionConfig(
            model=self.model,
            encoding=self.audio_encoding(),
            sample_rate_hertz=self.sample_rate_hertz,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            language_code=self.language_code,
            use_enhanced=self.use_enhanced,
            alternative_language_codes=self.alternate_language_codes,
            audio_channel_count=self.audio_channel_count,
            enable_separate_recognition_per_channel=self.enable_separate_recognition_per_channel,
            enable_spoken_punctuation=self.enable_spoken_punctuation,
            enable_spoken_emojis=self.enable_spoken_emojis,
            max_alternatives=self.max_alternatives,
            speech_contexts=self.speech_context(),
            enable_word_confidence=self.enable_word_confidence,
            metadata=self.recognition_meta_data()
        )
        return config_mp3

    def read_audio(self, path=r"Recording.mp3"):
        record()
        try:
            if path is not None:
                with open(path, 'rb') as f:
                    byte_data_mp3 = f.read()
                audio_mp3 = speech.RecognitionAudio(content=byte_data_mp3)
                return audio_mp3
        except:
            return self.read_audio(path=r"Recording.mp3")

    def generate_text(self):
        self.check_for_bounds()
        if self.state == True:
            try:
                speech_client = speech.SpeechClient()
                audio_mp3 = self.read_audio()
                try:
                    response_standard_mp3 = speech_client.recognize(
                        config=self.create_reg_config(),
                        audio=audio_mp3)
                    os.remove("Recording.mp3")
                    return response_standard_mp3.results[0].alternatives[0].transcript

                except:
                    response_standard_mp3 = speech_client.long_running_recognize(
                        config=self.create_reg_config(),
                        audio=audio_mp3
                    )
                    os.remove("Recording.mp3")
                    return response_standard_mp3.result().results[0].alternatives[0].transcript
            except:
                return self.generate_text()

        else:
            raise ValueError("Speech Parameters Invalid")

    @staticmethod
    def load_phrase_set(file_path: str):
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            loaded_data = yaml.safe_load(yaml_file)
            return loaded_data

    def speech_context(self):
        if self.speech_context_path is not None:
            speech_context = self.load_phrase_set(self.speech_context_path)
            return speech_context
        else:
            return None

    def check_speech_context(self):
        speech_context = self.speech_context()
        if speech_context is not None:
            for i in speech_context:
                if (i.get("boost") > 20 or i.get("boost") < 0):
                    self.state = False

    def recognition_meta_data(self):
        metadata = speech.RecognitionMetadata(
            interaction_type=self.select_interaction_type(),
            industry_naics_code_of_audio=self.naics_code,
            microphone_distance=self.select_microphone_distance(),
            original_media_type=self.select_media_type(),
            recording_device_name=self.recording_device_name,
            recording_device_type=self.select_recording_device_type(),
            audio_topic=self.audio_topic
        )
        return metadata

    def select_interaction_type(self):
        if (self.interaction_type == "discussion"):
            return speech.RecognitionMetadata.InteractionType.DISCUSSION
        elif (self.interaction_type == "presentation"):
            return speech.RecognitionMetadata.InteractionType.PRESENTATION
        elif (self.interaction_type == "phone_call"):
            return speech.RecognitionMetadata.InteractionType.PHONE_CALL
        elif (self.interaction_type == "voice_mail"):
            return speech.RecognitionMetadata.InteractionType.VOICEMAIL
        elif (self.interaction_type == "professionally_produced"):
            return speech.RecognitionMetadata.InteractionType.PROFESSIONALLY_PRODUCED
        elif (self.interaction_type == "voice_search"):
            return speech.RecognitionMetadata.InteractionType.VOICE_SEARCH
        elif (self.interaction_type == "voice_command"):
            return speech.RecognitionMetadata.InteractionType.VOICE_COMMAND
        elif (self.interaction_type == "dictation"):
            return speech.RecognitionMetadata.InteractionType.DICTATION
        else:
            return speech.RecognitionMetadata.InteractionType.INTERACTION_TYPE_UNSPECIFIED

    def select_microphone_distance(self):
        if (self.microphone_distance == "nearfield"):
            return speech.RecognitionMetadata.MicrophoneDistance.NEARFIELD
        elif (self.microphone_distance == "midfield"):
            return speech.RecognitionMetadata.MicrophoneDistance.MIDFIELD
        elif (self.microphone_distance == "farfield"):
            return speech.RecognitionMetadata.MicrophoneDistance.FARFIELD
        else:
            return speech.RecognitionMetadata.MicrophoneDistance.MICROPHONE_DISTANCE_UNSPECIFIED

    def select_media_type(self):
        if (self.original_media_type == "audio"):
            return speech.RecognitionMetadata.OriginalMediaType.AUDIO
        elif (self.original_media_type == "video"):
            return speech.RecognitionMetadata.OriginalMediaType.VIDEO
        else:
            return speech.RecognitionMetadata.OriginalMediaType.ORIGINAL_MEDIA_TYPE_UNSPECIFIED

    def select_recording_device_type(self):
        if (self.recording_device_type == "smartphone"):
            return speech.RecognitionMetadata.RecordingDeviceType.SMARTPHONE
        elif (self.recording_device_type == "pc"):
            return speech.RecognitionMetadata.RecordingDeviceType.PC
        elif (self.recording_device_type == "phone_line"):
            return speech.RecognitionMetadata.RecordingDeviceType.PHONE_LINE
        elif (self.recording_device_type == "vehicle"):
            return speech.RecognitionMetadata.RecordingDeviceType.VEHICLE
        elif (self.recording_device_type == "other_outdoor_device"):
            return speech.RecognitionMetadata.RecordingDeviceType.OTHER_OUTDOOR_DEVICE
        elif (self.recording_device_type == "other_indoor_device"):
            return speech.RecognitionMetadata.RecordingDeviceType.OTHER_INDOOR_DEVICE
        else:
            return speech.RecognitionMetadata.RecordingDeviceType.RECORDING_DEVICE_TYPE_UNSPECIFIED

    def check_for_bounds(self):
        self.check_speech_context()