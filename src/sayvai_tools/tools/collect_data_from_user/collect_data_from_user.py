from typing import Type, Optional, Dict

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, create_model, Field


def create_data_model(fields: Dict[str, str]) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model from the fields dictionary.

    :param fields: A dictionary where keys are field names and values are descriptions.
    :return: A dynamically created Pydantic model.
    """
    field_definitions = {field: (str, Field(description=desc)) for field, desc in fields.items()}
    return create_model('UserData', **field_definitions)


class CollectUserDataTool(BaseTool):
    name: str = "user_data_collector"
    description: str = "Collects data from the user based on specified fields."

    args_schema: Type[BaseModel]

    def _run(self, run_manager: Optional[CallbackManagerForToolRun] = None, **kwargs) -> bool:
        try:
            # Validate data using the dynamically created model
            print("Collected and validated data:", kwargs)
            return True
        except Exception as e:
            print("Error in data collection or validation:", str(e))
            return False
