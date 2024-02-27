import datetime

from langchain.tools import BaseTool

from sayvai_tools.utils.exception import SayvaiToolsError


class GetDate(BaseTool):
    """Get the current date and time."""

    name = "GetDate"
    description = "Get the current date and time."

    @classmethod
    def create(cls) -> "GetDate":
        return cls()

    def _run(self, tool_input: str | None = None) -> str:
        """Use the tool."""
        current_time = datetime.datetime.now()
        return str(current_time)

    async def _arun(self) -> str:
        """Use the tool asynchronously."""
        raise SayvaiToolsError("Not NotImplemented Error")
