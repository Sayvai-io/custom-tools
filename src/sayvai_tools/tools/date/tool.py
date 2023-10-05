import datetime


class GetDate:

    def _run(self, tool_input: str) -> str:
        """Use the tool."""
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%A, %B %d, %Y %I:%M %p")
        return formatted_time

    async def _arun(self, tool_input: str) -> str:
        """Use the tool asynchronously."""
        raise("Not NotImplemented Error")
        # return None

