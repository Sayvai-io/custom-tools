# tool for forms
from typing import Any, Dict, List

from sayvai_tools.utils.google.forms import GForms


class FormTool:
    def __init__(self, scope: str, title: str = "Test Form"):
        self.scope = scope
        self.form = GForms(formTitle=title)

    name = "Form Tool"
    description = "Tool for forms"

    def _run(self, questions: List[str]):
        self.form.add_multiple_questions(questions=questions)
        return "Questions have been added"

    def _arun(self):
        pass
