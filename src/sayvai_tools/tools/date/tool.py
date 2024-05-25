from datetime import datetime
from typing import Optional

from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun


class GetDate(BaseTool):
    name: str = "get_current_date_time"
    description: str = "Gets the current date and time."

    @classmethod
    def create(cls) -> "GetDate":
        return cls()

    def _run(self, 
            run_manager: Optional[CallbackManagerForToolRun] = None
            ) -> str:
        current_time = datetime.now()
        return str(current_time)

