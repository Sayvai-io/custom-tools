from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_forms.base import GoogleFormsBaseTool


class CreateFormSchema(BaseModel):
    """Input schema for CreateFormTool."""

    title: str = Field(
        ...,
        description="Title of the form to be created.",
    )
    document_title: Optional[str] = Field(
        None,
        description="Document title of the form to be created.",
    )


class CreateFormTool(GoogleFormsBaseTool):
    """Tool for creating a Google Form."""

    name: str = "create_google_form"
    description: str = "Use this tool to create a Google Form."
    args_schema: Type[CreateFormSchema] = CreateFormSchema

    def _create_empty_form(
        self,
        title: str,
        document_title: Optional[str] = None,
    ) -> str:
        """Create an empty Google Form with the specified title and document title.

        Args:
            title: Title of the form.
            document_title: Document title of the form (optional).

        Returns:
            URL of the created form.
        """
        form = {"title": title, "documentTitle": document_title}
        created_form = self.api_resource.forms().create(body=form).execute()
        return created_form["formUrl"]

    def _run(
        self,
        title: str,
        document_title: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            # Create an empty form
            form_url = self._create_empty_form(title, document_title)

            # Extract form ID from form URL
            form_id = form_url.split("/")[-1]

            return form_id
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
