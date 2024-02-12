import datetime

from sayvai_tools.utils.exception import SayvaiToolsError


class GetDate:

    @classmethod
    def create(cls) -> "GetDate":
        return cls()

    def _run(self, tool_input: str | None = None) -> str:
        """Use the tool."""
        current_time = datetime.datetime.now()
        return current_time

    async def _arun(self) -> str:
        """Use the tool asynchronously."""
        raise SayvaiToolsError("Not NotImplemented Error")
