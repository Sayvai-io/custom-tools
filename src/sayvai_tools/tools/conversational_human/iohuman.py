"""Conversational Human """
from typing import Callable, Optional
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import Field
from elevenlabs import play
from sayvai_tools.utils.tts import ElevenlabsAudioStreaming
from sayvai_tools.utils.stt import STT



# def _print_func(text: str) -> None:
#     print("\n")
#     print(text)


class ConversationalHuman:
    """Tool that asks user for input."""

    name: str = "human"
    description: str = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )
    # prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    # input_func: Callable = Field(default_factory=lambda: input)
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.stt = STT(audio_format="mp3")
        self.tts = ElevenlabsAudioStreaming()
        pass

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""

        inputbytes = self.tts.audio_streaming(query,
                            model="eleven_multilingual_v1",
                            voice="Adam", 
                            audio_streaming= True, 
                            stability= 0.5,
                            similarity= 0.5,
                            api_key= self.api_key)
        play(inputbytes)

        # self.prompt_func(query)
        # return self.input_func()
        return(self.stt.generate_text().result().results[0].alternatives[0].transcript)
