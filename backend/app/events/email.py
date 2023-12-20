import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.app.config.settings import get_settings

settings = get_settings()


class EmailEvent:
    def __init__(self):
        self._email = settings.EMAIL_USER
        self._host = settings.EMAIL_USER
        self._password = settings.EMAIL_PASSWORD
        self._port = settings.EMAIL_PORT

    def send_email(self, boddy: str, to: str, subject: str) -> None:
        """Send email."""
        message = MIMEMultipart("alternative")
        message["From"] = self._email
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(boddy, "html"))

        server = smtplib.SMTP(self._host, port=self._port)
        server.starttls()
        server.login(self._email, self._password)
        server.sendmail(self._email, to, message.as_string())
        server.quit()
