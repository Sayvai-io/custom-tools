"""base tool for IO"""

from elevenlabs import play
from sayvai_tools.utils.voice.tts import ElevenlabsAudioStreaming


class VoiceOutputRun:
    """Tool that asks user for input."""

    name: str = "voice"
    description: str = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        assert isinstance(self.api_key, str)
        pass

    @classmethod
    def create(cls, api_key: str) -> cls:
        return cls(api_key)

    def _run(
        self,
        query: str,
    ):
        """Use the Human input tool."""
        # input_func: Callable = Field(default_factory=lambda: input)
        tts = ElevenlabsAudioStreaming(self.api_key)
        input_bytes = tts.audio_streaming(
            query,
            model="eleven_multilingual_v1",
            voice="Adam",
            audio_streaming=True,
            stability=0.5,
            similarity=0.5,
        )
        play(input_bytes)
