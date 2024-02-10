import datetime

from sayvai_tools.utils.exception import SayvaiToolsError


class GetDate:

    @classmethod
    def create(cls) -> "GetDate":
        return cls()

    def _run(self) -> str:
        """Use the tool."""

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%A, %B %d, %Y %I:%M %p")
        return formatted_time

    async def _arun(self) -> str:
        """Use the tool asynchronously."""
        raise SayvaiToolsError("Not NotImplemented Error")
