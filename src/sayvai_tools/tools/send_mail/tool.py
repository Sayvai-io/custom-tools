# Author: Aathikabilan
import os
import aysncio
from sayvai_tools.utils import EmailSender
from sayvai_tools.utils import Excel

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ORGANIZER_EMAIL = os.getenv("ORGANIZER_EMAIL")

class SendMail:
    name = "send_mail"
    description = "You can ask send_mail tool to send mail for you."

    def __init__(self, path: str):
        self.excel = Excel(path=path)
        self.emails = self.excel.read_column("email")
        self.email_sender = EmailSender(ORGANIZER_EMAIL, SMTP_USERNAME, SMTP_PASSWORD)

    def _run(self, content: str):
        self.email_sender.send_multiple_email(self.emails, "Sayvai", content)
        return "Mail sent successfully"

    async def _arun(self, content: str):
        raise NotImplementedError("Send mail via async not implemented")