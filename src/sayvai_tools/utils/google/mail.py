import smtplib
import ssl
from email.message import EmailMessage


class EmailSender:
    def __init__(self, organizer_email, smtp_username, smtp_password):
        self.organizer_email = organizer_email
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465  # SSL port

    def send_email(self, receiver_email, subject, message):
        em = EmailMessage()
        em.set_content(message)
        em["Subject"] = subject
        em["From"] = self.organizer_email
        em["To"] = receiver_email

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(
                self.smtp_server, self.smtp_port, context=context
            ) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.organizer_email, receiver_email, em.as_string())
                print("Email sent successfully")
        except Exception as e:
            print(e)
            
    def send_multiple_email(self, receiver_emails, subject, message):
        for receiver_email in receiver_emails:
            self.send_email(receiver_email, subject, message)
        
